import os
import requests
import http.server
import socketserver

def simple_server(directory:str, port:int):
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)
    httpd.serve_forever()

def download_to_file(download_url:str, file_name:str, directory:str):
        
    file_path = os.path.join('data', 'libraries', directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    response = requests.get(download_url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        print("[ERROR] file not found: " + download_url)

def simplify_classpath(classpath:str):
    """
    removes preceding path of classpath used in compilation for simplified output:
    e.g.: data/libraries/commons-beanutils/commons-beanutils-1.9.2.jar:data/libraries/commons-collections/commons-collections-3.2.1.jar
    returns commons-beanutils-1.9.2.jar:commons-collections-3.2.1.jar

    @param classpath:
    @return: simplified classpath String   
    """

    dependencies = classpath.split(":")
    for i in range(0, len(dependencies)):
        d = dependencies[i].split("/") 
        dependencies[i] = d[len(d) - 1].replace(".jar", "")  

    return ":".join(dependencies)

