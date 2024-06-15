# java-deserialization-rce
An In-depth Study of Java Deserialization Remote-Code Execution Exploits and Vulnerabilities


Generated files are available here https://www.dropbox.com/sh/qu9hr6jv446zcja/AACtNVUCrlBl9ZGk-mdfG3dka?dl=0

# Coverage

| Exploit | Completion | Description |
| ----- | ----- | ----- |
| AspectJWeaver  |  ✅  | as a file write exploit, can also be exploited with simple payload for file name | 
 | BeanShell1 |  ✅  | simple rce | 
 | C3P0 |  ✅  | implementation through launching simple python server serving remote class to create proof.txt file | 
 | Click1 |  ✅  | simple rce  | 
 | Clojure |  ✅   | simple rce | 
 | CommonsBeanutils1 |  ✅  | simple rce  | 
 | CommonsCollections1 | ✅  | simple rce  | 
 | CommonsCollections2 |  ✅  | simple rce   | 
 | CommonsCollections3 |  ✅  | simple rce  | 
 | CommonsCollections4 |  ✅  | simple rce  | 
 | CommonsCollections5 |  ✅  |  simple rce | 
 | CommonsCollections6 |  ✅  | simple rce  | 
 | CommonsCollections7 |  ✅  | simple rce  | 
 | FileUpload1 |  ✅  | arbitrary filename, but destination folder is controllable, thus exploit can also be easily validated | 
 | Groovy1 |  ✅  | simple rce  | 
 | Hibernate1 |  ✅  |  | 
 | Hibernate2 |  ✅ |  | 
 | JBossInterceptors1 |  ✅  | The javax-interceptor api at version 3.1 is missing on maven repo https://mvnrepository.com/artifact/javax.interceptor/javax.interceptor-api/3.1, however this is no issue since exploit also works with 1.2 | 
 | JRMPClient |  ✅  | reverse shell setup with sockets | 
 | JRMPListener |  ✅  | bind shell setup with sockets | 
 | JSON1 |  ✅  | simple rce  | 
 | JavassistWeld1 |  ✅  | simple rce  | 
 | Jdk7u21 |  ✅  | simple rce  | 
 | Jython1 |  ✅  | simple python script in /src/scripts being executed | 
 | MozillaRhino1 |  ✅  | simple rce  | 
 | MozillaRhino2 |  ✅  | simple rce  | 
 | Myfaces1 |  ❌  |  | 
 | Myfaces2 |  ❌  |  | 
 | ROME |  ✅  | simple rce  | 
 | Spring1 |  ✅  | simple rce  | 
 | Spring2 |  ✅  | simple rce  | 
 | URLDNS |  ✅  | launch tcpdump in background and pipe dns requests for specific domain name into file, then check file for content | 
 | Vaadin1 |  ✅  | simple rce  | 
 | Wicket1 |  ✅  | simple rce  | 

 # newgadgets branch:

 
| Exploit | Completion | Description |
| ----- | ----- | ----- |
 | Ceylon |  ✅  | simple rce | 
 | CommonsCollections8 |  ✅  | simple rce |
 | CommonsBeanUtils2 |  ✅  | simple rce |
 | Clojure2 |  ✅  | simple rce |
 | Jython2| ✅ | simple rce |
 | Atomikos | ✅ | rmi |

 33/35


