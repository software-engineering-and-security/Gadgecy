import os
import re

class Result_Item:
    def __init__(self, name):
        self.cnt = 0
        self.name = name
        self.projects = []

    def __str__(self):
        return "\\textbf{" + self.name + "} & " + str(self.cnt) + " & " + str(self.projects) + "\\\\"


data = open(os.path.join("..", "data", "apache-projects-raw", "results_raw.txt"), "r").readlines()
results = {}
project_cnt = []

for line in data:
    project = line.split(" ")[1].split("/")[-1]
    payload = line.split(" ")[7].replace(":", "")

    deps = re.sub(r"(.*\[)|([',\]\n])", "", line).split(" ")

    if project not in project_cnt:
        project_cnt.append(project)

    if payload not in results:
        results[payload] = Result_Item(payload)

    results[payload].cnt += 1
    results[payload].projects.append(project)

results = sorted(results.items(), key=lambda item : item[1].cnt, reverse=True)

for item in results:
    print(item[1])

print(len(project_cnt))


