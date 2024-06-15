class Payload:
    def __init__(self, name:str, type:str, dependencies:list[str], fixpoints:list[str]):
        self.name = name
        self.type = type
        self.dependencies = dependencies
        self.fixpoints = fixpoints


class Payloads:
    AspectJWeaver = Payload( "AspectJWeaver" , "file-write" , 
                            ["aspectjweaver","commons-collections"],
                           ["1.9.2", "3.2.2"])
    Atomikos = Payload("Atomikos", "rmi", ["transactions-osgi", "jta"], ["4.0.6", "1.1"])
    BeanShell = Payload( "BeanShell1" , "rce" , ["bsh"], ["2.0b5"])
    C3P0 = Payload( "C3P0" , "remote-class" , 
                    ["c3p0","mchange-commons-java"],
                    ["0.9.5.2", "0.2.11"])
    Ceylon = Payload("Ceylon", "rce", ["ceylon.language"], ["1.3.3"])
    Click1 = Payload( "Click1" , "rce" , 
                    ["click-nodeps","servlet-api"],
                    ["2.3.0", "3.1.0"] )
    Clojure = Payload( "Clojure" , "rce" , ["clojure"], ["1.8.0"])
    Clojure2 = Payload("Clojure2" , "rce" , ["clojure"], ["1.8.0"])
    CommonsBeanutils1 = Payload( "CommonsBeanutils1" , "rce" , 
                                ["commons-beanutils","commons-collections","commons-logging"],
                                ["1.9.2", "3.1", "1.2"] )
    CommonsBeanutils2 = Payload( "CommonsBeanutils2" , "rce" , ["commons-beanutils", "commons-logging"], ["1.9.2", "1.2"])
    CommonsCollections1 = Payload( "CommonsCollections1" , "rce" , ["commons-collections"], ["3.1"])
    CommonsCollections2 = Payload( "CommonsCollections2" , "rce" , ["commons-collections"], ["4.0"])
    CommonsCollections3 = Payload( "CommonsCollections3" , "rce" , ["commons-collections"], ["3.1"])
    CommonsCollections4 = Payload( "CommonsCollections4" , "rce" , ["commons-collections"], ["4.0"])
    CommonsCollections5 = Payload( "CommonsCollections5" , "rce" , ["commons-collections"], ["3.1"])
    CommonsCollections6 = Payload( "CommonsCollections6" , "rce" , ["commons-collections"], ["3.1"])
    CommonsCollections7 = Payload( "CommonsCollections7" , "rce" , ["commons-collections"], ["3.1"])
    CommonsCollections8 = Payload( "CommonsCollections8" , "rce" , ["commons-collections"], ["4.0"])
    CreateZeroFile = Payload("CreateZeroFile", "zero-file", ["scala-library"], ["2.12.6"])
    Ssrf = Payload("Ssrf", "web-request", ["scala-library"], ["2.12.6"])
    FileUpload1 = Payload( "FileUpload1" , "file-upload" , 
                            ["commons-fileupload","commons-io"], 
                            ["1.3.1", "2.4"] )
    Groovy1 = Payload( "Groovy1" , "rce" , ["groovy"], ["2.3.9"] )
    Hibernate1 = Payload( "Hibernate1" , "rce" , 
                         ["hibernate-core", "aopalliance", "jboss-logging", "transaction-api", "dom4j"], 
                         ["5.0.7.Final", "1.0", "3.3.0.Final", "1.2", "1.6.1"] )
    Hibernate2 = Payload( "Hibernate2" , "rmi" , 
                         ["hibernate-core", "aopalliance", "jboss-logging", "transaction-api", "dom4j"], 
                         ["4.3.9.Final", "1.0", "3.3.0.Final", "1.2", "1.6.1"] )
    JBossInterceptors1 = Payload( "JBossInterceptors1" , "rce" , 
                                 ["javassist","jboss-interceptor-core","cdi-api","javax.interceptor-api","jboss-interceptor-spi","slf4j-api"],
                                 ["3.12.1.GA", "2.0.0.Final", "1.0-SP1", "1.2", "2.0.0.Final", "1.7.21"] )
    JRMPClient = Payload( "JRMPClient" , "jrmp-client" , [], [] )
    JRMPListener = Payload( "JRMPListener" , "jrmp-listener" , [], [] )
    JSON1 = Payload( "JSON1" , "rce" , 
                    ["json-lib","spring-aop","aopalliance","commons-logging","commons-lang","ezmorph","commons-beanutils","spring-core","commons-collections"],
                    ["2.4-jdk15", "4.1.4.RELEASE", "1.0", "1.2", "2.6", "1.0.6", "1.9.2", "4.1.4.RELEASE", "3.1"])
    JavassistWeld1 = Payload( "JavassistWeld1" , "rce" , 
                             ["javassist","weld-core","cdi-api","javax.interceptor-api","jboss-interceptor-spi","slf4j-api"],
                             ["3.12.1.GA", "1.1.33.Final", "1.0-SP1", "1.2", "2.0.0.Final", "1.7.21"] )
    Jdk7u21 = Payload( "Jdk7u21" , "rce" , [], [] )
    Jython1 = Payload( "Jython1" , "python-script-execution" , ["jython-standalone"], ["2.5.2"] )
    Jython2 = Payload( "Jython2" , "rce" , ["jython-standalone"], ["2.5.2"] )
    Jython3 = Payload( "Jython3" , "rce" , ["jython-standalone"], ["2.7.3"] )
    Jython4 = Payload( "Jython4", "rce", ["jython"], ["2.7.2b2"])
    MozillaRhino1 = Payload( "MozillaRhino1" , "rce" , ["js"], ["1.7R2"] )
    MozillaRhino2 = Payload( "MozillaRhino2" , "rce" , ["js"], ["1.7R2"] )
    Myfaces1 = Payload( "Myfaces1" , "rce" ,
                        ["myfaces-impl", "myfaces-api", "apache-el", "servlet-api", "mockito-core", "hamcrest-core", "objenesis"], 
                        ["2.2.9", "2.2.9", "8.0.27", "3.1.0", "1.10.19", "1.1", "2.1"])
    Myfaces2 = Payload( "Myfaces2" , "rce" , 
                       ["myfaces-impl", "myfaces-api", "apache-el", "servlet-api", "mockito-core", "hamcrest-core", "objenesis"], 
                        ["2.2.9", "2.2.9", "8.0.27", "3.1.0", "1.10.19", "1.1", "2.1"])
    ROME = Payload( "ROME" , "rce" , ["rome"], ["1.0"] )
    ROME2 = Payload( "ROME2", "rce", ["rome"], ["1.0"] )
    Spring1 = Payload( "Spring1" , "rce" , 
                      ["spring-core","spring-beans"],
                      ["4.1.4.RELEASE", "4.1.4.RELEASE"])
    Spring2 = Payload( "Spring2" , "rce" , 
                      ["spring-core","spring-aop","aopalliance","commons-logging"],
                      ["4.1.4.RELEASE", "4.1.4.RELEASE", "1.0", "1.2"])
    SpringJta = Payload( "SpringJta" , "rmi" , 
                      ["spring-core", "spring-beans","spring-tx","spring-context", "jta", "commons-logging"],
                      ["5.1.7.RELEASE", "5.1.7.RELEASE","5.1.7.RELEASE","5.1.7.RELEASE", "1.1", "1.2"])
    Struts2JasperReports = Payload("Struts2JasperReports", "rce", ["struts2-core", "struts2-jasperreports-plugin"], ["2.5.20", "2.5.20"] )
    URLDNS = Payload( "URLDNS" , "dns-lookup" , [], [])
    Vaadin1 = Payload( "Vaadin1" , "rce" , 
                        ["vaadin-server","vaadin-shared"],
                        ["7.7.14", "7.7.14"]  )
    Wicket1 = Payload( "Wicket1" , "rmi" , 
                      ["wicket-util","slf4j-api"],
                      ["6.23.0", "1.6.4"])
    WildFly = Payload("WildFly", "rmi", ["wildfly-connector"], ["30.0.1.FINAL"])
    Lazylist = Payload("Lazylist", "lazylist", 
                      ["scala-library"],["2.13.8"]  )

