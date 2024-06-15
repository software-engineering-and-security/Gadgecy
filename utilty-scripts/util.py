import os
import shutil
import tarfile
from zipfile import ZipFile
import jellyfish
import re


def extract_tar(filename : str, destination_name : str) -> None:
    with tarfile.open(filename, 'r') as tar:
        tar.extractall(destination_name)


def extract_jar(filename : str, destination_name : str) -> None:
    with ZipFile(filename, 'r') as zipfile:
        zipfile.extractall(destination_name)


def extract(filename: str, destination_name: str):
    f_split = filename.split(".")
    if f_split[len(f_split) - 1] in ["jar", "zip"]:
        extract_jar(filename, destination_name)
    elif ".tar.gz" in filename or ".tgz" in filename:
        extract_tar(filename, destination_name)
    else:
        print(f"[ERROR] File {filename} is no tar/jar file")


def get_classpath_from_dir(dirname: str) -> list:
    classpath = []
    for file in os.listdir(os.path.join(dirname, "lib")):
        path = os.path.join(dirname, "lib", file)
        if os.path.isfile(path) and ".jar" in path:
            classpath.append(path)

    return classpath


def get_application_jars_from_project(dirname : str) -> list:
    project_name = dirname.split(os.sep)[len(dirname.split(os.sep)) - 1]
    jar_files = []

    if not "lib" in os.listdir(dirname):
        print(f"[INFO] {dirname} contains no lib folder, skipping")
    else:
        libpath = os.path.join(dirname, "lib")
        for file in os.listdir(libpath):
            if not ".jar" in file:
                continue

            file_name = file.replace(".jar", "")
            file_name = re.sub(r'-(\d\.)+\d(\.((RELEASE)|(Release)|(FINAL)|(Final)))?',"", file_name)
            f_split = file_name.split(".")
            if len(f_split) >= 2:
                file_name = f_split[len(f_split) - 1]

            if jellyfish.jaro_similarity(project_name, file_name.replace(".jar", "")) >= 0.6:
                jar_files.append(file)

    return jar_files


def get_jar_version(jar_file):

    file_parts = os.path.split(jar_file)
    directory = os.path.join(file_parts[0], "tmp")
    file_split = file_parts[1].split("-")
    v_test = file_split[len(file_split) - 1].replace(".jar", "")

    if re.search(r"(\d\.)+\d", v_test):
        return v_test
    if re.search(r"(\d\.)+\d\.((Final)|(RELEASE)|(FINAL)|(Release))", v_test):
        return v_test

    version = ""

    extract_jar(jar_file, directory)
    if os.path.exists(os.path.join(directory, "META-INF", "maven")):
        mvn_info_path = os.path.join(directory, "META-INF", "maven")
        try:
            # looking for file META-INF/maven/<artifact_name>/<artifact_name>/pom.properties
            artifact_path_1 = os.path.join(mvn_info_path, os.listdir(mvn_info_path)[0])
            artifact_path_2 = os.path.join(artifact_path_1, os.listdir(artifact_path_1)[0])
            pom_properties = os.path.join(artifact_path_2, "pom.properties")

            with open(pom_properties, 'r') as properties_file:
                data = properties_file.read()
                for line in data.split("\n"):
                    if "version" in line:
                        version = line.split("=")[1]
                        break

        except:
            print("[Error] pom.properties not found in " + jar_file)
    else:
        print("[Error] Version could not be determined for " + jar_file)

    shutil.rmtree(directory)
    return version
