import re
import xml.etree.ElementTree as ET


class Pom_Dependency:
    def __init__(self, name, group, version):
        self.name = name
        self.group = group
        self.version = version

    def has_version(self):
        return self.version != ""

    def __str__(self):
        return self.name + "-" + self.version

    def __repr__(self):
        return self.name + "-" + self.version

def get_dependencies(pom, namespace, scope=None) -> list[Pom_Dependency]:
    dependencies = []

    for dependency in pom.findall(f".//{namespace}dependency"):
        dep_name = dep_version = dep_group = ""

        add_dependency = True

        for child in dependency:
            if scope is not None and "scope" in child.tag and child.text in scope:
                add_dependency = False
                break

            if "version" in child.tag:

                substitute = re.search(r"\$\{.*}", child.text)
                if substitute:
                    prop_name = re.sub(r"[${}]", "", substitute.group(0))

                    if prop_name == "project.version":
                        if pom.find(f"./{namespace}version") is not None:
                            dep_version = pom.find(f"./{namespace}version").text

                    elif pom.find(f".//{namespace}{prop_name}") is not None:
                        dep_version = pom.find(f".//{namespace}{prop_name}").text

                else:
                    dep_version = child.text

            elif "groupId" in child.tag:
                dep_group = child.text
            elif "artifactId" in child.tag:
                dep_name = child.text

        if add_dependency and dep_name != "":
            dependencies.append(Pom_Dependency(dep_name, dep_group, dep_version))

    return dependencies


def parse_pom(path, scope=None) -> list[Pom_Dependency]:
    root = ET.parse(path).getroot()
    xml_namespace = ""
    if re.match(r'\{.*\}', root.tag):
        xml_namespace = re.match(r'\{.*\}', root.tag).group(0)

    return get_dependencies(root, xml_namespace, scope=scope)