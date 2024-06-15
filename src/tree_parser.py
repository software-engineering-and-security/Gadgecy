import re
import subprocess
from src import dependencies as payload_dependencies

'''
from command: mvn depedency:tree -f pom.xml -doutputType=dot -B

Format definition:

{
"project_name": {
    "module_name": {
        "vuln_dependencies" : [
        {
            "dependency" : "commons-beanutils",
            "version" : "1.9.4",
            "chain" : ["hadoop", "other_dep"]
        }


        ],

        "payloads" : ["CommonsBeanutils", ...]

    }
}
}
'''


def populate_payloads(project):
    for module in project:
        module_obj = project[module]["vuln_dependencies"]

        for payload in payload_dependencies.PAYLOADS:
            hit_deps = []

            for vuln_dep_obj in module_obj:
                for payload_dep in payload.dependencies:
                    if payload_dep.name in vuln_dep_obj["dependency"] and vuln_dep_obj["version"] in payload_dep.versions:
                        if not payload_dep.name in hit_deps:
                            hit_deps.append((vuln_dep_obj["dependency"], vuln_dep_obj["version"]))
                        break
                if len(hit_deps) >= len(payload.dependencies):
                    break

            if len(hit_deps) >= len(payload.dependencies):
                if not "payloads" in project[module]:
                    project[module]["payloads"] = []
                project[module]["payloads"].append(payload.name)
                for hit_dep in hit_deps:
                    for vuln_dep_obj in module_obj:
                        if hit_dep[0] == vuln_dep_obj["dependency"] and hit_dep[1] == vuln_dep_obj["version"]:
                            if not "enables_payload" in vuln_dep_obj:
                                vuln_dep_obj["enables_payload"] = []
                            vuln_dep_obj["enables_payload"].append(payload.name)

    return project


def mvn_tree(file_path, output_to_console=True):
    result = {}
    module_name = ""
    module_obj = {}
    appended = []
    p = subprocess.Popen(["mvn", "dependency:tree", "-f", file_path, "-DoutputType=dot", "-B"], stdout=subprocess.PIPE)

    while True:
        line = p.stdout.readline().decode("utf-8")
        if not line:
            if module_obj:
                result[module_name] = module_obj
            break

        if re.search(r"-+<\s.*\s>-+", line):
            if module_obj:
                result[module_name] = module_obj
            try:
                module_name = re.search(r"< [A-Za-z0-9_:.-]* >", line).group(0).replace("<", "").replace(">",
                                                                                                         "").strip()
            except:
                print(line)
                exit(1)
            module_obj = {}
            appended = []

        if '" -> "' in line:
            chain = []
            for line_dep in re.findall(r'"[A-Za-z0-9_:.-]*"', line):
                line_dep = line_dep.replace('"', '')
                if line_dep.split(":")[-1] == "test":
                    continue

                line_dep_package = line_dep.split(":")[0]
                line_dep_name = line_dep.split(":")[1]
                line_dep_version = line_dep.split(":")[3]
                chain.append(f"{line_dep_package}:{line_dep_name}:{line_dep_version}")

                if payload_dependencies.is_vulnerable_dependency(line_dep_name, line_dep_version) and f"{line_dep_name}-{line_dep_version}" not in appended:
                    if not "vuln_dependencies" in module_obj:
                        module_obj["vuln_dependencies"] = []


                    module_obj["vuln_dependencies"].append({
                        "dependency": line_dep_name,
                        "version": line_dep_version,
                        "chain": chain
                    })
                    appended.append(f"{line_dep_name}-{line_dep_version}")

    result = populate_payloads(result)

    return result

