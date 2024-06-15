import json
import os.path
import time
from datetime import datetime
import sys

import requests
import xml.etree.ElementTree as ET
import re
from src import dependencies as payload_dependencies


# TODO: implement parsing of gradle files
# TODO: import remaining payloads (with version ranges) into payloads


def download_modules(base_url, base_directory, module_name):

    response = requests.get(f"{base_url}/pom.xml")
    if 200 <= response.status_code < 300:
        main_dir = os.path.join(base_directory, module_name)
        os.makedirs(main_dir, exist_ok=True)
        open(os.path.join(main_dir, "pom.xml"), "w").write(response.text)

        root = ET.fromstring(response.text)
        xml_namespace = ""

        if re.match(r'\{.*\}', root.tag):
            xml_namespace = re.match(r'\{.*\}', root.tag).group(0)

        for module in root.findall(f".//{xml_namespace}module"):
            download_modules(f"{base_url}/{module.text}", main_dir, module.text)



module_cnt = 0
star_limit=100
skipped_projects = []

# get apache repos with 100+ stars and java lang
base_url = "https://raw.githubusercontent.com"
header = {}
if sys.argv[1]:
    header = {"Authorization" : f"Bearer {sys.argv[1]}",
          "X-GitHub-Api-Version": "2022-11-28"}



github_organisations = ["apache", "google", "android", "facebook", "spring-projects", "elastic", "TheAlgorithms", "ReactiveX",
                        "airbnb", "alibaba", "dbeaver", "bumptech", "netty", "zxing", "SeleniumHQ", "apolloconfig",
                        "dromara", "termux", "TeamNewPipe", "seata", "signalapp", "Netflix", "libgdx", "redisson",
                        "jenkinsci", "bazelbuild", "oracle", "mybatis", "Baseflow", "keycloak", "Tencent", "openzipkin",
                        "antlr", "material-components", "thingsboard", "mockito", "arduino", "deeplearning4j", "GoogleContainerTools",
                        "java-decompiler", "pinpoint-apm", "questdb", "quarkusio", "projectlombok", "neo4j", "Yalantis", "zaproxy",
                        "redis", "realm", "androidannotations", "supertokens", "square", "clojure", "OpenRefine", "languagetool-org",
                        "Activiti", "jwtk", "resilience4j", "SonarSource", "trello", "flyway", "provectus", "NanoHttpd", "beemdevelopment",
                        "MinecraftForge", "Alluxio", "zendesk", "processing", "junit-team", "graphql-java", "roboelectric", "StarRocks",
                        "hazelcast", "hibernate", "btraceio", "journeyapps", "auth0", "AntennaPod", "lettuce-io", "lingochamp",
                        "eclipse", "sonatype", "jitsi", "geogebra", "strongbox", "TEAMMATES", "JabRef", "commons-app", "xwiki", "sirixdb", "PhilJay"
                        , "greenrobot", "Blankj", "nostra13", "skylot"]

commit_ids = []

for org in github_organisations:

    results_arr = []

    response = requests.get(f"https://api.github.com/search/repositories?per_page=100&q=language:java+stars%3A%3E100+org:{org}", headers=header)
    # github api request throtteling
    while response.status_code >= 300:
        time.sleep(2)
        response = requests.get(f"https://api.github.com/search/repositories?per_page=100&q=language:java+stars%3A%3E100+org:{org}", headers=header)

    for item in response.json()["items"]:

        # skip unmaintained projects
        update_year = int(item["updated_at"].split("-")[0])
        if update_year <= 2022 or item["archived"] or "updated_at" not in item:
            print("old-> " + item["name"])
            continue

        print(item["name"])
        default_branch = item["default_branch"]

        sub_url = f'{org}/{item["name"]}/{default_branch}'
        response = requests.get(f"{base_url}/{sub_url}/pom.xml")

        if 200 <= response.status_code < 300:

            main_dir = os.path.join("pom", f'{org}-{item["name"]}')
            ####
            if not os.path.exists(main_dir):
                continue

            commit_response = requests.get(f"https://api.github.com/repos/{org}/{item['name']}/commits/{default_branch}", headers=header)

            while response.status_code >= 300:
                time.sleep(2)
                commit_response = requests.get(f"https://api.github.com/repos/{org}/{item['name']}/commits/{default_branch}", headers=header)

            commit_id = commit_response.json()["sha"]
            commit_ids.append({f'{org}-{item["name"]}' : commit_id})

            os.mkdir(main_dir)
            open(os.path.join(main_dir, "pom.xml"), "w").write(response.text)

            root = ET.fromstring(response.text)
            xml_namespace = re.match(r'\{.*\}', root.tag).group(0)

            for module in root.findall(f".//{xml_namespace}module"):
                download_modules(f"{base_url}/{sub_url}/{module.text}",main_dir, module.text)

        else:
            print(f'[WARN] project {item["name"]} contains no pom.xml')
            skipped_projects.append([org, item["name"]])

        print()

json.dump(commit_ids, open(os.path.join("results", "commits.json"), "w"), indent=4)
print(skipped_projects)
print(f"[INFO] Total modules scanned {module_cnt}")
