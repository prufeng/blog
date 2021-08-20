Logback SMTPAppender Send Mail When Log Error
====

>The SMTPAppender relies on the JavaMail API. It has been tested with JavaMail API version 1.4. The JavaMail API requires the JavaBeans Activation Framework package. 

```xml
<configuration>   
  <appender name="EMAIL" class="ch.qos.logback.classic.net.SMTPAppender">
    <evaluator class="ch.qos.logback.classic.boolex.OnErrorEvaluator" />
    <smtpHost>${smtpHost}</smtpHost>
    <to>${to}</to>
    <from>${from}</from>
    <subject>%logger{20} - %m</subject>
    <layout class="ch.qos.logback.classic.html.HTMLLayout"/>

    <cyclicBufferTracker class="ch.qos.logback.core.spi.CyclicBufferTracker">
      <!-- send just one log entry per email -->
      <bufferSize>1</bufferSize>
    </cyclicBufferTracker>
  </appender>

  <root level="DEBUG">
    <appender-ref ref="EMAIL" />
  </root>  
</configuration>   
```

# OnErrorEvaluator
默認ERROR以上才send email，重寫即可改變觸發條件，比如遇到指定Exception。

>If the Evaluator property is not set, the SMTPAppender defaults to an OnErrorEvaluator instance which triggers email transmission when it encounters an event of level ERROR. While triggering an outgoing email in response to an error is relatively reasonable, it is possible to override this default behavior by providing a different implementation of the EventEvaluator interface.

```java
public class OnErrorEvaluator extends EventEvaluatorBase<ILoggingEvent> {

    /**
     * Return true if event passed as parameter has level ERROR or higher, returns
     * false otherwise.
     */
    public boolean evaluate(ILoggingEvent event) throws NullPointerException, EvaluationException {
        return event.getLevel().levelInt >= Level.ERROR_INT;
    }
}
```

# OnMarkerEvaluator
根據Logger參數決定是否send mail。
```java
Marker notifyAdmin = MarkerFactory.getMarker("NOTIFY_ADMIN");
logger.error(notifyAdmin,
  "This is a serious an error requiring the admin's attention",
   new Exception("Just testing"));
```
```xml
<configuration>
  <appender name="EMAIL" class="ch.qos.logback.classic.net.SMTPAppender">
    <evaluator class="ch.qos.logback.classic.boolex.OnMarkerEvaluator">
      <marker>NOTIFY_ADMIN</marker>
      <!-- you specify add as many markers as you want -->
      <marker>TRANSACTION_FAILURE</marker>
    </evaluator>
    <smtpHost>${smtpHost}</smtpHost>
    <to>${to}</to>
    <from>${from}</from>
    <layout class="ch.qos.logback.classic.html.HTMLLayout"/>
  </appender>

  <root>
    <level value ="debug"/>
    <appender-ref ref="EMAIL" />
  </root>  
</configuration>
```
## Other Appenders
http://logback.qos.ch/manual/appenders.html

* FileAppender, RollingFileAppender
* SocketAppender, SSLSocketAppender
* ServerSocketAppender, SSLServerSocketAppender
* DBAppender 
* SyslogAppender
* SiftingAppender
