Springboot想动态使用指定范围内的端口，可以实现WebServerFactoryCustomizer

除了端口，WebServerFactoryCustomizer还可以改address，error pages等，也就是ConfigurableWebServerFactory可以设置的东西。

>Strategy interface for customizing web server factories. Anybeans of this type will get a callback with the server factory before the server itselfis started, so you can set the port, address, error pages etc. 
Beware: calls to this interface are usually made from a WebServerFactoryCustomizerBeanPostProcessor which is a BeanPostProcessor (so called very early in the ApplicationContext lifecycle).It might be safer to lookup dependencies lazily in the enclosing BeanFactory ratherthan injecting them with @Autowired.

代码比较简单，这里的setPort()会覆盖默认的server.port的值。
```
@Component
public class CustomContainer implements WebServerFactoryCustomizer<ConfigurableWebServerFactory> {

	@Value("${server.port.list}")
	private String serverPortList;

	@Override
	public void customize(ConfigurableWebServerFactory factory) {
		factory.setPort(selectOnePort(this.serverPortList));
	}

	private int selectOnePort(String ports) throws IllegalStateException {
        // TODO
        // Get available port list
        // Select one port from available list
	}
}
```
