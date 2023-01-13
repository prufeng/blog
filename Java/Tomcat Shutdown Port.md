官网解释：
>The TCP/IP port number on which this server waits for a shutdown command. Set to -1 to disable the shutdown port.

>Note: Disabling the shutdown port works well when Tomcat is started using Apache Commons Daemon (running as a service on Windows or with jsvc on un*xes). It cannot be used when running Tomcat with the standard shell scripts though, as it will prevent shutdown.bat|.sh and catalina.bat|.sh from stopping it gracefully.

默认开启，telnet后直接输入SHUTDOWN，可成功关闭Tomcat。
```
telnet localhost 8005
SHUTDOWN
```
```
13-Jan-2023 09:58:26.140 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 5073 ms
13-Jan-2023 09:59:07.574 WARNING [main] org.apache.catalina.core.StandardServer.await Invalid shutdown command [SSH-2.0-PuTTY_Release_0.70] received
13-Jan-2023 09:59:42.034 WARNING [main] org.apache.catalina.core.StandardServer.await Invalid shutdown command [S] received
13-Jan-2023 09:59:54.320 INFO [main] org.apache.catalina.core.StandardServer.await A valid shutdown command was received via the shutdown port. Stopping the Server instance.
13-Jan-2023 09:59:54.320 INFO [main] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
13-Jan-2023 09:59:54.391 INFO [main] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
```
禁用之后，使用命令行无法关闭Tomcat。

停止Tomcat的脚本依赖于这个端口的服务功能。这样是不是不太好？
```
<Server port="-1" shutdown="SHUTDOWN">
```
```
shutdown.bat
```
```
13-Jan-2023 10:06:18.553 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 5039 ms
13-Jan-2023 10:06:32.117 SEVERE [main] org.apache.catalina.startup.Catalina.stopServer No shutdown port configured. Shut down server through OS signal. Server not shut down.
```
