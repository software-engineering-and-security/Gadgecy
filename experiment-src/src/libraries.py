import requests
from bs4 import BeautifulSoup
from . import util

MAVEN_REPO_URL = "https://repo1.maven.org/maven2"
libraries ={

    "ceylon.language" : "org/ceylon-lang/ceylon.language",
    "wildfly-connector" : "org/wildfly/wildfly-connector",
    
    "commons-collections" :[
       ["commons-collections", "commons-collections/commons-collections"],
      ["commons-collections4", "org/apache/commons/commons-collections4"] 
    ], 

    "struts2-core" : "org/apache/struts/struts2-core",
    "struts2-jasperreports-plugin" : "org/apache/struts/struts2-jasperreports-plugin",

    "scala-library" :[
          [ "scala-library", "org/scala-lang/scala-library"], 
           ["scala3-library_3", "org/scala-lang/scala3-library_3"] 
    ], 


    "transactions-osgi" : "com/atomikos/transactions-osgi",
    "jta" : "javax/transaction/jta",

    "spring-tx": "org/springframework/spring-tx",
    "spring-context": "org/springframework/spring-context",

    "myfaces-impl" : [
        ["myfaces-impl" , "org/apache/myfaces/core/myfaces-impl"],
        ["myfaces-impl" , "myfaces/myfaces-impl"]
    ],
    "myfaces-api" : [
    
    ["myfaces-api", "org/apache/myfaces/core/myfaces-api"],
    ["myfaces-api", "myfaces/myfaces-api"]
    ],
    "apache-el" : "org/mortbay/jasper/apache-el",
    "aspectjweaver" : [        
        ["aspectjweaver", "org/aspectj/aspectjweaver"],
        ["aspectjweaver", "aspectj/aspectjweaver"]
     ],
    "bsh" : [
        ["bsh", "bsh/bsh"],
        ["bsh","org/apache-extras/beanshell/bsh" ],
        [ "bsh", "org/beanshell/bsh"]
    ],
    "c3p0" : [
        ["c3p0", "com/mchange/c3p0"],
        ["c3p0", "c3p0/c3p0"]
    ],
    "mchange-commons-java" : "com/mchange/mchange-commons-java",
    "click-nodeps" : [
        ["click-nodeps","org/apache/click/click-nodeps"],
        ["click-nodeps", "net/sf/click/click-nodeps"]

     ],
     "dom4j" : [
        [ "dom4j", "dom4j/dom4j"],
        ["dom4j", "org/dom4j/dom4j"]   


     ],
    "servlet-api" : [
        
        ["javax.servlet-api","javax/servlet/javax.servlet-api"],
        ["servlet-api", "javax/servlet/servlet-api"]

    ],
    "clojure" : "org/clojure/clojure",
    "commons-beanutils" : "commons-beanutils/commons-beanutils",
    "commons-logging" : "commons-logging/commons-logging",
    "commons-fileupload" : "commons-fileupload/commons-fileupload",
    "commons-io" : "commons-io/commons-io",
    "groovy" : [
        
        ["groovy", "org/codehaus/groovy/groovy"],
        ["groovy", "org/apache/groovy/groovy"]
    ],
    "javassist" :[ 
       [ "javassist","org/javassist/javassist"] ,
        [ "javassist", "javassist/javassist"] 
    ],
    "jboss-interceptor-core" : "org/jboss/interceptor/jboss-interceptor-core",
    
    # both libs belong to cdi-api, starting with version 3 moved to jakarta-enterprise:
    "cdi-api" :[
        [ "cdi-api","javax/enterprise/cdi-api" ],
        [ "jakarta.enterprise.cdi-api","jakarta/enterprise/jakarta.enterprise.cdi-api" ] 
    ],

    # download link for javax.interceptor-api 3.0 missing ...
    "javax.interceptor-api" : "javax/interceptor/javax.interceptor-api",

    "jboss-interceptor-spi" : "org/jboss/interceptor/jboss-interceptor-spi",
    "slf4j-api" : "org/slf4j/slf4j-api",
    "json-lib" : "net/sf/json-lib/json-lib",
    "spring-aop" : "org/springframework/spring-aop",
    "aopalliance" : "aopalliance/aopalliance",
    
    # both libs belong to commons-lang, starting with version 3 moved to commons-lang3:
    "commons-lang" :[
        ["commons-lang","commons-lang/commons-lang"] ,
        ["commons-lang3","org/apache/commons/commons-lang3"] 
    ],

    "ezmorph" : "net/sf/ezmorph/ezmorph",
    "spring-core" : "org/springframework/spring-core",
    "weld-core": "org/jboss/weld/weld-core",
    "jython-standalone": "org/python/jython-standalone",
    "jython": "org/python/jython",

    # yet again two links to js/rhino lib
    "js":[
        ["js","rhino/js"],
        ["rhino","org/mozilla/rhino"]  
    ],

    # also two repo links
    "rome" : [
        ["rome","rome/rome"],
        ["rome","com/rometools/rome"] 
    ],

    "spring-beans" : "org/springframework/spring-beans",
    "vaadin-server" : "com/vaadin/vaadin-server",
    "vaadin-shared" : "com/vaadin/vaadin-shared",
    "wicket-util" : "org/apache/wicket/wicket-util",
    "hibernate-core" : [
        ["hibernate-core", "org/hibernate/hibernate-core"],
        ["hibernate-core", "org/hibernate/orm/hibernate-core"]
],
"transaction-api": [    
    ["javax.transaction-api","javax/transaction/javax.transaction-api"],
    ["jakarta.transaction-api", "jakarta/transaction/jakarta.transaction-api"]
],
    "jboss-logging" : "org/jboss/logging/jboss-logging"

} 

def generate_jar_name(lib:str, version:str):
    if lib == "json-lib" and int(version.split('.')[0]) >= 1:
        return [
            lib + '-' + version + '-jdk13.jar',
            lib + '-' + version + '-jdk15.jar'
        ]
    
    return [lib + '-' + version + '.jar'] 

def download(lib_name:str, lib_url:str, directory:str):
    count = 0    
    url = "{}/{}".format(MAVEN_REPO_URL, lib_url)
    page = requests.get(url)
    print("[INFO] Downloading from " + url)
    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all('a'):
        version = link.text.replace('/', '')
        if "maven-metadata" in version or '..' in version:
            continue
        
        
        jar_names = generate_jar_name(lib_name, version)
        # workaround for json lib having 2 types per version
        for jar_name in jar_names:
            download_url = "/".join([url, version, jar_name])
            count = count + 1
            
            # download invocation here
            util.download_to_file(download_url, jar_name, directory)

    return count

def download_all(filter:list[str]=None): 
    count = 0
    
    for lib in libraries:

        if filter != None and not lib in filter:
            continue

        # Certain libraries have been moved after a certain version number within the maven repo
        if type(libraries[lib]) == list:
            for lib_subtype in libraries[lib]:
                count += download(lib_subtype[0] , lib_subtype[1] , lib)

        else:
            count += download(lib, libraries[lib], directory=lib)

    return count

def get_library_count():
    print()
    return len(libraries)

