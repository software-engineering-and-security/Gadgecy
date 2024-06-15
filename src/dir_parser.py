import hashlib
import os.path
from glob import glob


def check_jar_file(path, hashes):
    if not os.path.isfile(path):
        return None

    file_hash = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            file_hash.update(data)

    for dep_hash in hashes:
        if dep_hash[1] == file_hash.hexdigest():
            return dep_hash[0]

    return None


def check_directory(path, hashes):
    findings = []

    jar_files = glob(f"{path}/**/*.jar", recursive=True)
    for jar_file in jar_files:
        finding = check_jar_file(jar_file, hashes)
        if finding is not None:
            findings.append(finding)

    return findings