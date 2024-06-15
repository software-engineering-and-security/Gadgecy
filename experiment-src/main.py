import sys
import os

from src import libraries as lib
from src import runner as runner
from src.payloads import Payloads
from src.results import Result



if len(sys.argv) >= 2:
    
    payload = None
    all_payloads = {}
    for p in vars(Payloads):
        if not "__" in p:
            all_payloads[p] = vars(Payloads)[p]

    # prepare the remote class serving
    if sys.argv[1] == "PrepareRMI":
        runner.prepare_rmi(runner.REMOTE_CLASS_SERVER_PORT)    

    elif sys.argv[1] in all_payloads.keys():
        payload = all_payloads[sys.argv[1]]
    else:
        print("[ERROR] unknown payload option")

    # second argument is for payload constraint vendor:version,version,version
    if payload:
        if sys.argv[2]:
            runner.run_payload_group_all(payload, sys.argv[2])
        else:
            runner.run_payload_group_all(payload)
    elif sys.argv[1] == "results":
        Result.write_to_files()
    elif sys.argv[1] == "lib":
        lib.download_all()
    elif sys.argv[1] == "run-count":
        for p in all_payloads:
            runs = 1
            base_dir = os.path.join("data", "libraries")
            dependencies = all_payloads[p].dependencies
            for dep in dependencies:
                dir = len(os.listdir(os.path.join(base_dir, dep)))
                runs += dir
            print(f"{p} : {runs}")

# print(lib.download("commons-collections4", "org/apache/commons/commons-collections4", "commons-collections"))
#runner.run_single("", "data/libraries/commons-collections/commons-collections4-4.0.jar", "CommonsCollections4")

#print(lib.download_all())
#runner.run_optimal(Payloads.Hibernate1, "", debug=True)
#runner.run_payload_group_all(Payloads.CommonsCollections1)
#runner.run_payload_group(Payloads.JavassistWeld1, "")
#runner.run_optimal(Payloads.CommonsCollections6, "/home/jvm/oracle/8/jdk1.8.0_241", debug=True)


