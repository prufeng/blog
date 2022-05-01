# Tomcat报错
27-Jan-2022 14:09:07.450 信息 [main] org.apache.coyote.AbstractProtocol.start 开始协议处理句柄["https-jsse-nio-8443"]
27-Jan-2022 14:09:07.459 严重 [main] org.apache.catalina.util.LifecycleBase.handleSubClassException 无法启动组件[Connector[AJP/1.3-8009]]
    org.apache.catalina.LifecycleException: 协议处理器启动失败
        at org.apache.catalina.connector.Connector.startInternal(Connector.java:1075)
        at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:183)
        at org.apache.catalina.core.StandardService.startInternal(StandardService.java:449)
        at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:183)
        at org.apache.catalina.core.StandardServer.startInternal(StandardServer.java:927)
        at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:183)
        at org.apache.catalina.startup.Catalina.start(Catalina.java:772)
        at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.lang.reflect.Method.invoke(Method.java:498)
        at org.apache.catalina.startup.Bootstrap.start(Bootstrap.java:345)
        at org.apache.catalina.startup.Bootstrap.main(Bootstrap.java:476)
    Caused by: java.lang.IllegalArgumentException: AJP连接器配置secretRequired="true",但是属性secret确实空或者空字符串，这样的组合是无效的。
        at org.apache.coyote.ajp.AbstractAjpProtocol.start(AbstractAjpProtocol.java:270)
        at org.apache.catalina.connector.Connector.startInternal(Connector.java:1072)
        ... 12 more


vi conf/server.xml

<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />


直接设置`secretRequired=""`可以解决，不过这种办法似乎不应该提倡，因为default是true。

不如加一个密码， `secret='secret'`

# secret	
Only requests from workers with this secret keyword will be accepted. The default value is null. This attribute must be specified with a non-null, non-zero length value unless secretRequired is explicitly configured to be false. If this attribute is configured with a non-null, non-zero length value then the workers must provide a matching value else the request will be rejected irrespective of the setting of secretRequired.

# secretRequired	
If this attribute is true, the AJP Connector will only start if the secret attribute is configured with a non-null, non-zero length value. This attribute only controls whether the secret attribute is required to be specified for the AJP Connector to start. It does not control whether workers are required to provide the secret. The default value is true. This attribute should only be set to false when the Connector is used on a trusted network.
