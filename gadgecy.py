import argparse
import json
import os
from src import dependencies as payload_dependencies
from src import dir_parser, pom_parser, tree_parser
from colorama import Fore, Style

HASH_FILE_NAME = "hash.json"

def print_colored(text, color):
    print(color + text + Style.RESET_ALL)

def print_info(text):
    print_colored(text, Fore.WHITE)

def print_error(text):
    print_colored(text, Fore.LIGHTRED_EX)


def print_warning(text):
    print_colored(text, Fore.LIGHTYELLOW_EX)


def print_banner():
    print_colored((' ________      ________      ________      ________      _______       ________       ___    ___ ' + '\n'
     r'|\   ____\    |\   __  \    |\   ___ \    |\   ____\    |\  ___ \     |\   ____\     |\  \  /  /|' + '\n'
     r'\ \  \___|    \ \  \|\  \   \ \  \_|\ \   \ \  \___|    \ \   __/|    \ \  \___|     \ \  \/  / /' + '\n'
     r' \ \  \  ___   \ \   __  \   \ \  \ \\ \   \ \  \  ___   \ \  \_|/__   \ \  \         \ \    / / ' + '\n'
     r'  \ \  \|\  \   \ \  \ \  \   \ \  \_\\ \   \ \  \|\  \   \ \  \_|\ \   \ \  \____     \/  /  /  ' + '\n'
     r'   \ \_______\   \ \__\ \__\   \ \_______\   \ \_______\   \ \_______\   \ \_______\ __/  / /    ' + '\n'
     r'    \|_______|    \|__|\|__|    \|_______|    \|_______|    \|_______|    \|_______||\___/ /     ' + '\n'
     r'                                                                                    \|___|/      ' + '\n')
                  , Fore.LIGHTGREEN_EX)


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=  "A tool for detecting whether your project contains the dependencies containing gadgets in known "
                  "Java Deserialization payloads from the ysoserial repository.",
    epilog="Example of use: \n"
           "\tpython gadgecy.py --pom project/pom.xml --scope test\n"
           "\tpython gadgecy.py --project project_dir --export results.json"
)

parser.add_argument("--setup", action="store_true", help="Downlods the critical dependency file hashes and saves them to hash.json")
parser.add_argument("--pom", nargs=1, help="<path/to/pom.xml>")
parser.add_argument("--mvn", nargs=1, help="<path/to/pom.xml>, requires maven to be installed")
parser.add_argument("--jar", nargs=1, help="<path/to/dependency.jar> - returns whether jar file is used within a payload")
parser.add_argument("--project", nargs=1, help="<path/to/project_root> - parses all jar files within project and checks if a combination used within a payload is met")
parser.add_argument("--export", nargs=1, help="<outputfile.json> - writes output into json file")
parser.add_argument("--scope", nargs=1, help="<excludeScope1,excludeScope2> - used with --pom to exclude scanning e.g. dependencies scoped within test")
parser.add_argument("--nobanner", action="store_true", help="don't display banner")
parser.parse_args()
args = parser.parse_args()

if not args.nobanner:
    print_banner()

result = None

if args.setup:
    print_info(f"Downloading sha1-hashes for dependencies and versions defined in ./payloads from maven repository. This may take a while")
    hash_sums = payload_dependencies.get_checksums("payloads")
    print_info(f"collected {len(hash_sums)} unique jar file sha1-hashes")
    with open(HASH_FILE_NAME, "w") as file:
        file.write(json.dumps(hash_sums))

if args.pom:
    scope = None
    if args.scope:
        scope = args.scope[0].split(",")
        print_info(f"Ignoring scoped items f{scope}")
    else:
        print_info(f"No scope defined, I will also include pom dependencies listed as test, etc.")

    dependencies = pom_parser.parse_pom(args.pom[0], scope=scope)
    for dep in dependencies:
        for payload in payload_dependencies.PAYLOADS:
            hit_list = []

            for p_d in payload.dependencies:
                if dep.name in p_d.name:
                    if dep.version == "":
                        print_warning(f"Version ({args.pom[0]}) for dependency {dep.name} could not be determined from pom.xml, but is used in payloads")
                    elif dep.version in p_d.versions:
                        hit_list.append(f"{dep.name}-{dep.version}")
                    break

            if len(hit_list) >= len(payload.dependencies):
                print_error(f"Project {args.pom[0]} contains gadgets used in Payload {payload.name}: {hit_list}")


elif args.mvn:
    result = tree_parser.mvn_tree(args.mvn[0])

    for module in result:
        if "payloads" in result[module]:
            flat_dependencies = []
            for dep in result[module]['vuln_dependencies']:
                flat_dependencies.append(f"{dep['dependency']}-{dep['version']}")
            print_error(f"Project {args.mvn[0]}, submodule: {module} contains gadgets used in Payload(s) {result[module]['payloads']}: {flat_dependencies}")


elif args.project:
    hashes = json.load(open(HASH_FILE_NAME, "r"))
    if not os.path.exists(HASH_FILE_NAME):
        print_error(f"[ERROR] could not find {HASH_FILE_NAME}")
        exit(1)

    if args.jar:
        result = dir_parser.check_jar_file(args.jar[0], hashes)
        print(payload_dependencies.get_containing_payloads(result))

    elif args.project:
        dependencies = dir_parser.check_directory(args.project[0], hashes)
        result = payload_dependencies.get_payloads(dependencies)
        for payload in result:
            print_error(f"Project {args.project[0]} contains gadgets used in Payload {payload[0]}: {payload[1]}")


if args.export and result is not None:
    print_info(f"Exporting findings to {args.export[0]}")
    with open(args.export[0], "w") as file:
        file.write(json.dumps(result, indent=4))

