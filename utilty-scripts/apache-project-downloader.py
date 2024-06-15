import requests
from bs4 import BeautifulSoup
import re
import os

BASE_URL = "https://dlcdn.apache.org/"

DIR_BLACKLIST = ["c", "cpp", "python", "js", "doc", "docs", "txt"]
FILE_BLACKLIST = ["source", "src", "site-docs", "win.zip", "mac-64bit", "javadoc", "windows", "-win-", "-mac-"]


def download_project_from_path(path:str, download_dir:str, use_project_dir=True):
    path_split = path.split("/")
    project_name = path_split[0]
    file_name = path_split[len(path_split) - 1]

    response = requests.get(BASE_URL + "/" + path)

    if use_project_dir:
        if not os.path.exists(os.path.join(download_dir, project_name)):
            os.mkdir(os.path.join(download_dir, project_name))
        download_path = os.path.join(download_dir, project_name, file_name)
    else:
        download_path = os.path.join(download_dir, file_name)

    open(download_path, 'wb').write(response.content)
    return download_path


def get_project_names() -> list:
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    projects = []
    for link in soup.find_all("a"):
        if "/" in link.text:
            projects.append(link.text)

    return projects


def is_directory(dirname: str) -> bool:
    if not "/" in dirname:
        return False
    if dirname.replace("/", "") in DIR_BLACKLIST:
        return False

    return True


def is_zip_file(filename: str) -> bool:
    if "/" in filename:
        return False
    for blacklist_file in FILE_BLACKLIST:
        if blacklist_file in filename:
            return False

    if re.search(r"((\.gz)|(\.tgz)|(\.jar)|(\.zip))$", filename):
        return True

    return False


def get_project_download_links(project_name: str, subdir: str = "/") -> list:
    project_name = project_name.replace("/", "")
    download_links = []
    response = requests.get(BASE_URL + project_name + subdir, allow_redirects=False)

    if 300 <= response.status_code <= 400:
        print(f"[WARNING] Redirect when querying {project_name}, propably archived - skipping.")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all("a"):
        if is_directory(link.text):
            download_links += get_project_download_links(project_name, subdir + link.text)
        elif is_zip_file(link.text):
            download_links.append(project_name.replace("/", "") + subdir + link.text)

    return download_links
