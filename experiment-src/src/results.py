import os
import json
import re
from .libraries import libraries

class Dependency:
    def __init__(self, dependency_name:str):
        self.name = dependency_name
        self.versions = [] 

    def add_version(self, version:str):
        self.versions.append(version)

    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} : {self.versions}"    


class JDK_Entry:

    def __init__(self, jdk_name:str, dependencies:list[str]):
        self.name = jdk_name
        self.dependencies = [] 

        for d in dependencies:
            self.dependencies.append(Dependency(d))

        self.exploitable = False

    def add_classpath(self, classpath:str):          
        self.exploitable = True
        if len(self.dependencies) == 0:
            return
        
        classpath_deps = classpath.split("#")

        for i in range(0, len(classpath_deps)): 
            name = self.dependencies[i].get_name()          
            self.dependencies[i].add_version( classpath_deps[i].replace(name + "-", "")
                                             .replace(name, "")
                                             .replace(".jar", "")) 

    def __str__(self):
        string = f"-----{self.name}-----\n "
        for d in self.dependencies:
            string += f"{d}\n"
        return string

class Result:

    def __init__(self, payload_name:str):
        self.name = payload_name
        self.entries = [] 

    def add_jdk_version(self, jdk_version:JDK_Entry):
        self.entries.append(jdk_version)

    def write_to_files(output_directory="data/json", input_directory="output"):        

        file_obj = {} 

        for file in os.listdir(input_directory):
            if not os.path.isfile(os.path.join(input_directory, file)):
                continue

            f_split = file.split("_")
            exploit_name = f_split[0]
            jdk_version = f_split[1]
            classpath = f_split[2]

            if re.search("^\d+\d$", f_split[2]):
                jdk_version = f_split[1] + "_" +  f_split[2]
                classpath = f_split[3]

            if not exploit_name in file_obj.keys():
                file_obj[exploit_name] = {}

            if not jdk_version in file_obj[exploit_name].keys():
                file_obj[exploit_name][jdk_version] = {}

            if classpath == "":
                continue

            classpath_split = classpath.split("#")
            for dependency in classpath_split:

                dependency_name = ""
                dependency_replace_name = ""

                for lib in libraries:
                    if lib in dependency:

                        dependency_name = lib

                        if isinstance(libraries[lib], list) and not lib == "commons-collections":
                            for sub_lib in libraries[lib]:
                                if sub_lib[0] in dependency_name:
                                    dependency_replace_name = sub_lib[0]
                                    break

                        else:
                            dependency_replace_name = dependency_name
                        

                dependency_version = dependency.replace(dependency_replace_name + "-", "").replace(dependency_replace_name, "").replace(".jar", "")

                if not dependency_name in file_obj[exploit_name][jdk_version].keys():
                    file_obj[exploit_name][jdk_version][dependency_name] = []

                exists = False

                for dv in file_obj[exploit_name][jdk_version][dependency_name]:
                    if dv == dependency_version:
                        exists = True
                        break
                
                if not exists:
                    file_obj[exploit_name][jdk_version][dependency_name].append(dependency_version)
        
        for exploit in file_obj:
            with open(os.path.join(output_directory, f"{exploit}.json"), "w") as out_file:
                out_file.write(json.dumps(file_obj[exploit], indent=4))

                  


              



    def write_to_file(self, file_name, output_directory="data/json", input_directory="output"):            

        file_object = {} 

        for jdk_entry in self.entries:
            file_object[jdk_entry.name] = {}  

            for dependency in jdk_entry.dependencies:
                file_object[jdk_entry.name][dependency.get_name()] = dependency.versions.copy()

        with open(os.path.join(output_directory, file_name + ".json" ), "w") as file:
            file.write(json.dumps(file_object, indent=4))



    def __str__(self):   
        string = ""     
        for e in self.entries:
            string += f"{e}\n"
        return string
