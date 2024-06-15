# Gadgecy
A tool and dataset for detecting dependencies used in known Java gadget chains.

This repository contains both the source code for the **Gadgecy** tool and the experiments which generated the dataset consumend by **Gadgecy**. If you are only interested in the tool check out the releases.

## Using Gadgecy

```bash
usage: gadgecy.py [-h] [--setup] [--pom POM] [--mvn MVN] [--jar JAR] [--project PROJECT] [--export EXPORT] [--scope SCOPE] [--nobanner]

A tool for detecting whether your project contains the dependencies containing gadgets in known Java Deserialization payloads from the ysoserial repository.

options:
  -h, --help         show this help message and exit
  --setup            Downlods the critical dependency file hashes and saves them to hash.json, this should be called at some point before using --jar or --project
  --pom POM          <path/to/pom.xml>
  --mvn MVN          <path/to/pom.xml>, requires maven to be installed
  --jar JAR          <path/to/dependency.jar> - returns whether jar file is used within a payload
  --project PROJECT  <path/to/project_root> - parses all jar files within project and checks if a combination used within a payload is met
  --export EXPORT    <outputfile.json> - writes output into json file
  --scope SCOPE      <excludeScope1,excludeScope2> - used with --pom to exclude scanning e.g. dependencies scoped within test
  --nobanner         don't display banner

Example of use:
        python gadgecy.py --pom project/pom.xml --scope test
        python gadgecy.py --project project_dir --export results.json
```

Using ``--mvn`` gives the most accurate results, since it resolves transitive dependencies using ``mvn dependency:tree``. Maven needs to be installed for this option.

## Dataset Generation

The JDKs used for the experiment are located located locally on a server under ``/home/jvm/<vendor>/<version>``. This path is hardcoded in the experiment scripts.

To run the experiments we start by downloading the dependency files from the maven repo.

```bash
python3 main.py lib
# Or specify which libraries to only download to speed up during updates
python3 main.py lib <inclusion-list>
python3 main.py lib spring-tx,spring-context
```

The download links are contained within ``src/libraries.py``. Then for running experiments the script takes two positional arguments ``python3 main.py <Payload> <jdk:version>``. This way parallel execution is split up using:

```bash
parallel --eta --ungroup python3 main.py ::: AspectJWeaver Atomikos BeanShell1 C3P0 Ceylon Click1 Clojure Clojure2 CommonsBeanutils1 CommonsBeanutils2 CommonsCollections1 CommonsCollections2 CommonsCollections3 CommonsCollections4 CommonsCollections5 CommonsCollections6 CommonsCollections7 CommonsCollections8 CreateZeroFile FileUpload1 Groovy1 Hibernate1 Hibernate2 JavassistWeld1 JBossInterceptors1 Jdk7u21 JRMPClient JRMPListener JSON1 Jython1 Jython2 Lazylist MozillaRhino1 MozillaRhino2 ROME Spring1 Spring2 SpringJta Ssrf Vaadin1 Wicket1 URLDNS ::: adoptium:8 adoptium:11 adoptium:16 adoptium:17 adoptium:18 adoptium:19 adoptium:20 adoptium:21 openjdk:9 openjdk:10 openjdk:11 openjdk:12 openjdk:13 openjdk:14 openjdk:15 openjdk:16 openjdk:17 openjdk:18 openjdk:19 openjdk:20 openjdk:21 oracle:6 oracle:7 oracle:9 oracle:10 oracle:12 oracle:13 oracle:14 oracle:15 oracle:16 oracle:17 oracle:18 oracle:19 oracle:20 oracle:21 ibm:0
```

This process will do the following for each dependencyversion-jdk-combination:

1. create a directory under ``output/`` named ``<Payload>_<jdk>_<dependency-1>-<version>_<dependency-2>-<version>_..._<dependency-n>-<version>_d`` containing the Victim class compiled using these dependencies and this JDK and any additional artefacts required for execution (e.g. a python script file for generating the proof file in **Jython1**).
2. generate the payload using the respective payload-generator jar file (3 x ysoserial and CVE-2022-36944 aka Lazylist) and also write it into a file inside the execution directory
3. execute the compiled java class using the given dependencies and jdk, which will on success create a proof file named ``<Payload>_<jdk>_<dependency-1>-<version>_<dependency-2>-<version>_..._<dependency-n>-<version>`` (same as directory without _d); the payload command is chosen in such a way as to generate a file named accordingly. In other cases a python subprocess socket listener will receive a request on success and then create the file.
4. cleanup - delete the directory and close any open sockets

We deviate from this procedure in the case of **Ssrf**, where we run ``python -m http.server 1025`` on a separate shell and then collect the terminal logs when the process is finished.

Finally we collect the results from the proof files using:

```bash
python3 main.py results
```

which dumps the data in a jdk-dependency coupled format into ``data/json``

### A note regarding the 4 Payload generators

|Generator | applicable payloads | description |
|-----|-----|-----|
| ysoserial-all.jar | AspectJWeaver BeanShell1 C3P0 Click1 Clojure CommonsBeanutils1 CommonsCollections1 CommonsCollections2 CommonsCollections3 CommonsCollections4 CommonsCollections5 CommonsCollections6 CommonsCollections7 FileUpload1 Groovy1 Hibernate1 Hibernate2 JavassistWeld1 JBossInterceptors1 Jdk7u21 JRMPClient JRMPListener JSON1 Jython1 MozillaRhino1 MozillaRhino2 ROME Spring1 Spring2 Vaadin1 Wicket1 URLDNS | the default build of Ysoserial |
| ysoserial-hibernate5.jar | Hibernate1 Hibernate2 | Ysoserial built using the -DHibernate5 option as described [here](https://medium.com/abn-amro-red-team/java-deserialization-from-discovery-to-reverse-shell-on-limited-environments-2e7b4e14fbef) |
| ysoserial-newgadgets.jar | Atomikos Ceylon Clojure2 CommonsBeanutils2 CommonsCollections8 CreateZeroFile Jython2 SpringJta Ssrf | Build of the new gadgets branch of ysoserial (with minor modifications to make it work; in particular reformating Scala payloads into two distinct files) |
| cve-2022-36944.jar | Lazylist | The PoC [here](https://github.com/yarocher/lazylist-cve-poc) built into a jar file |

## Experiments run with GNU parallel



```bash
ls data | parallel --ungroup python3 gadgecy.py --nobanner --project data/{}
```

```bash
ls -d */ | sed 's/\/$//' | parallel --eta "mvn dependency:tree -B -DoutputType=dot -f {}/pom.xml > {}.txt"
```
