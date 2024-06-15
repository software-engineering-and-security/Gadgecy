import requests
from bs4 import BeautifulSoup
import re
from . import util

def is_jdk(tag):
    return tag.has_attr('data-file') and re.search("jdk.*linux-x64", tag.text) and re.search("(rpm)|(deb)", tag.text) == None

def is_jdk_ge_17(tag):
    return tag.has_attr('href') and re.search("jdk.*linux-x64", tag.text) and re.search("(rpm)|(deb)", tag.text) == None


def download_oracle(authparam, url, version_number):
    count = 0
    base_download_url= "https://download.oracle.com"        

    response = requests.get('https://www.oracle.com' + url)
    soup = BeautifulSoup(response.content, "html.parser")    

    if version_number >= 17:            
        for link in soup.find_all(is_jdk_ge_17):
            print(link['href'])
            count += 1
    else:
        for link in soup.find_all(is_jdk):
            print("https:" + link["data-file"])
            count += 1
            # continue here : https://www.oracle.com/java/technologies/install-linux-64-self-extracting.html
    return count

def download_single_oracle(authparam):
    util.download_to_file("https://download.oracle.com/otn/java/jdk/7/jdk-7-linux-x64.tar.gz?AuthParam=" + authparam, "jdk-7-linux-x64.tar.gz", "data/jdk/jdk7")

def get_download_links_oracle(authparam, version_threshold=6):

    count = 0

    response = requests.get("https://www.oracle.com/java/technologies/downloads/archive/")
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all(href = re.compile("(jdk)|(javase)")):
        if re.search("Java SE \d", link.text):
            # cast to float because version links 1.x
            version_number = float(link.text.split(" ")[2])
            
            if version_number >= version_threshold: 
                count += download_oracle(authparam, link['href'], version_number)

    return count
