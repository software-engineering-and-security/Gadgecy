import os
import requests
import json
from tqdm import tqdm

LIB_URLS = {

    "ceylon.language": "org/ceylon-lang/ceylon.language",

    "commons-collections": "commons-collections/commons-collections",
    "commons-collections4": "org/apache/commons/commons-collections4",
    "struts2-core": "org/apache/struts/struts2-core",
    "struts2-jasperreports-plugin": "org/apache/struts/struts2-jasperreports-plugin",

    "scala-library": "org/scala-lang/scala-library",

    "transactions-osgi": "com/atomikos/transactions-osgi",
    "jta": "javax/transaction/jta",

    "spring-tx": "org/springframework/spring-tx",
    "spring-context": "org/springframework/spring-context",
    "myfaces-impl": [
        ["myfaces-impl", "org/apache/myfaces/core/myfaces-impl"],
        ["myfaces-impl", "myfaces/myfaces-impl"]
    ],
    "myfaces-api": [
        ["myfaces-api", "org/apache/myfaces/core/myfaces-api"],
        ["myfaces-api", "myfaces/myfaces-api"]
    ],
    "apache-el": "org/mortbay/jasper/apache-el",
    "mockito-core": "org/mockito/mockito-core",
    "hamcrest-core": "org/hamcrest/hamcrest-core",
    "objenesis": "org/objenesis/objenesis",

    "aspectjweaver": [
        ["aspectjweaver", "org/aspectj/aspectjweaver"],
        ["aspectjweaver", "aspectj/aspectjweaver"]
    ],
    "bsh": [
        ["bsh", "bsh/bsh"],
        ["bsh", "org/apache-extras/beanshell/bsh"],
        ["bsh", "org/beanshell/bsh"]
    ],
    "c3p0": [
        ["c3p0", "com/mchange/c3p0"],
        ["c3p0", "c3p0/c3p0"]
    ],
    "mchange-commons-java": "com/mchange/mchange-commons-java",
    "click-nodeps": [
        ["click-nodeps", "org/apache/click/click-nodeps"],
        ["click-nodeps", "net/sf/click/click-nodeps"]

    ],
    "dom4j": [
        ["dom4j", "dom4j/dom4j"],
        ["dom4j", "org/dom4j/dom4j"]

    ],
    "servlet-api": [
        ["javax.servlet-api", "javax/servlet/javax.servlet-api"],
        ["servlet-api", "javax/servlet/servlet-api"]
    ],
    "clojure": "org/clojure/clojure",
    "commons-beanutils": "commons-beanutils/commons-beanutils",
    "commons-logging": "commons-logging/commons-logging",
    "commons-fileupload": "commons-fileupload/commons-fileupload",
    "commons-io": "commons-io/commons-io",
    "groovy": [
        ["groovy", "org/codehaus/groovy/groovy"],
        ["groovy", "org/apache/groovy/groovy"]
    ],
    "javassist": [
        ["javassist", "org/javassist/javassist"],
        ["javassist", "javassist/javassist"]
    ],
    "jboss-interceptor-core": "org/jboss/interceptor/jboss-interceptor-core",

    # both libs belong to cdi-api, starting with version 3 moved to jakarta-enterprise:
    "cdi-api": [
        ["cdi-api", "javax/enterprise/cdi-api"],
        ["jakarta.enterprise.cdi-api", "jakarta/enterprise/jakarta.enterprise.cdi-api"]
    ],

    # download link for javax.interceptor-api 3.0 missing ...
    "javax.interceptor-api": "javax/interceptor/javax.interceptor-api",

    "jboss-interceptor-spi": "org/jboss/interceptor/jboss-interceptor-spi",
    "slf4j-api": "org/slf4j/slf4j-api",
    "json-lib": "net/sf/json-lib/json-lib",
    "spring-aop": "org/springframework/spring-aop",
    "aopalliance": "aopalliance/aopalliance",

    # both libs belong to commons-lang, starting with version 3 moved to commons-lang3:
    "commons-lang": [
        ["commons-lang", "commons-lang/commons-lang"],
        ["commons-lang3", "org/apache/commons/commons-lang3"]
    ],

    "ezmorph": "net/sf/ezmorph/ezmorph",
    "spring-core": "org/springframework/spring-core",
    "weld-core": "org/jboss/weld/weld-core",
    "jython-standalone": "org/python/jython-standalone",
    "jython": "org/python/jython",

    # yet again two links to js/rhino lib
    "js": [
        ["js", "rhino/js"],
        ["rhino", "org/mozilla/rhino"]
    ],

    # also two repo links
    "rome": [
        ["rome", "rome/rome"],
        ["rome", "com/rometools/rome"]
    ],

    "spring-beans": "org/springframework/spring-beans",
    "vaadin-server": "com/vaadin/vaadin-server",
    "vaadin-shared": "com/vaadin/vaadin-shared",
    "wicket-util": "org/apache/wicket/wicket-util",
    "hibernate-core": [
        ["hibernate-core", "org/hibernate/hibernate-core"],
        ["hibernate-core", "org/hibernate/orm/hibernate-core"]
    ],
    "transaction-api": [
        ["javax.transaction-api", "javax/transaction/javax.transaction-api"],
        ["jakarta.transaction-api", "jakarta/transaction/jakarta.transaction-api"]
    ],
    "jboss-logging": "org/jboss/logging/jboss-logging",
    "wildfly-connector": "org/wildfly/wildfly-connector",

}


def parse_dependency_string(dep_string):
    if "json-lib" in dep_string:
        return "json-lib", "-".join(dep_string.split("-")[-2:])

    dep_split = dep_string.split("-")
    dep_version = dep_split[-1]
    dep_name = dep_split[0]

    if len(dep_split) > 2:
        dep_name = "-".join(dep_split[0:-1])

    return dep_name, dep_version


class Dependency:
    def __init__(self, name: str, versions: list):
        self.name = name
        self.versions = versions


class Payload:
    def __init__(self, name: str, dependencies: list):
        self.dependencies = dependencies
        self.name = name

    def get_vulnerable(self, list_dependencies):

        hit_list = []
        dep_cnt = []

        for i in range(0, len(list_dependencies)):
            dep_name, dep_version = parse_dependency_string(list_dependencies[i])

            for vuln_dependency in self.dependencies:

                if dep_name == vuln_dependency.name and dep_version in vuln_dependency.versions:
                    hit_list.append(list_dependencies[i])
                    if dep_name not in dep_cnt:
                        dep_cnt.append(dep_name)
                    break
            if len(dep_cnt) >= len(self.dependencies):
                return hit_list

        return None


DEP_NAMES = ['ceylon.language', 'commons-collections', 'commons-collections4', 'struts2-core',
             'struts2-jasperreports-plugin', 'scala-library', 'transactions-osgi', 'jta', 'spring-tx', 'spring-context',
             'myfaces-impl', 'myfaces-api', 'apache-el', 'mockito-core', 'hamcrest-core', 'objenesis', 'aspectjweaver',
             'bsh', 'c3p0', 'mchange-commons-java', 'click-nodeps', 'dom4j', 'servlet-api', 'clojure',
             'commons-beanutils', 'commons-logging', 'commons-fileupload', 'commons-io', 'groovy', 'javassist',
             'jboss-interceptor-core', 'cdi-api', 'javax.interceptor-api', 'jboss-interceptor-spi', 'slf4j-api',
             'json-lib', 'spring-aop', 'aopalliance', 'commons-lang', 'ezmorph', 'spring-core', 'weld-core',
             'jython-standalone', 'js', 'rome', 'spring-beans', 'vaadin-server', 'vaadin-shared', 'wicket-util',
             'hibernate-core', 'transaction-api', 'jboss-logging']

# Generate Payloads from data:
PAYLOADS = []

for file in os.listdir("payloads"):
    payload_name = file.split(".")[0]
    dependencies = []

    with open(os.path.join("payloads", file), 'r') as f:
        data = json.loads(f.read())

    for key in data.keys():
        if key != "_jdk":
            dependencies.append(Dependency(key, data[key]))
    PAYLOADS.append(Payload(f"{payload_name}", dependencies))


def get_payloads(app_dependencies):
    vuln_payloads = []

    for payload in PAYLOADS:
        vuln_dep_list = payload.get_vulnerable(app_dependencies)

        if vuln_dep_list is not None:
            vuln_payloads.append([payload.name, vuln_dep_list])

    return vuln_payloads


def get_containing_payloads(dependency) -> list:
    containing_payloads = []
    dep_name, dep_version = parse_dependency_string(dependency)

    for payload in PAYLOADS:
        for p_d in payload.dependencies:
            if dep_name == p_d.name and dep_version in p_d.versions:
                containing_payloads.append(payload.name)
                break

    return containing_payloads


def is_vulnerable_dependency(dep_name, version) -> bool:
    # commons-beanutils:1.9.4 -> true
    for payload in PAYLOADS:
        for vuln_dep in payload.dependencies:
            if vuln_dep.name in dep_name and version in vuln_dep.versions:
                return True

    return False


BASE_URL = "https://repo1.maven.org/maven2"


def get_checksum_single(dependency_name: str, version: str):

    if type(LIB_URLS[dependency_name]) is list:
        for url in LIB_URLS[dependency_name]:
            response = requests.get(f"{BASE_URL}/{url[1]}/{version}/{url[0]}-{version}.jar.sha1")
            if 200 <= response.status_code < 300:
                return response.text
        return None
    else:
        # json-lib has multiple versions in the download dir of maven, therefor the version.split("-") ...
        if dependency_name == "json-lib":
            response = requests.get(f'{BASE_URL}/{LIB_URLS[dependency_name]}/{version.split("-")[0]}/{dependency_name}-{version}.jar.sha1')
        else:
            response = requests.get(f'{BASE_URL}/{LIB_URLS[dependency_name]}/{version}/{dependency_name}-{version}.jar.sha1')

        if 200 <= response.status_code < 300:
            return response.text
        print(f'{BASE_URL}/{LIB_URLS[dependency_name]}/{version.split("-")[0]}/{dependency_name}-{version}.jar.sha1')
        return None


def get_checksums(payload_dir="payloads") -> list:
    checksums = []

    for file in tqdm(os.listdir(payload_dir)):
        path = os.path.join(payload_dir, file)
        if os.path.isfile(path):
            data = json.load(open(path, "r"))
            for lib_name in data:
                if lib_name == "_jdk":
                    continue

                for version in data[lib_name]:
                    hash = get_checksum_single(lib_name, version)
                    if hash is None:
                        print(f"[WARN] Sha1 hash for {lib_name}-{version} could not be downloaded")
                    else:
                        hash = hash.split(" ")[0].strip()

                        # trim duplicates
                        append_hash = True
                        for h in checksums:
                            if h[1] == hash:
                                append_hash = False
                                break
                        if append_hash:
                            checksums.append([f"{lib_name}-{version}", hash])

    return checksums
