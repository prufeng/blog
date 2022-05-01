Spring - Schedule Task 如何动态改写Cron配置
---- 
使用Spring @Scheduled标签可以很简单地定义Scheduled Task，但是有时我们需要在程序里动态地改写Cron的配置。

什么时候呢？

额，比如：

老板觉得Cron配置太难看了，想直接这样：`10：15`

# Scheduling Tasks的常规使用
两个标签： `@EnableScheduling`， `@Scheduled`

```java
@SpringBootApplication
@EnableScheduling
public class SchedulingTasksApplication {

	public static void main(String[] args) {
		SpringApplication.run(SchedulingTasksApplication.class);
	}
}
```
```java
public class ScheduleTaskSimpleJob {

    @Scheduled(cron = "0 15 10 * * ?")
    public void scheduleCronTask() {
    
        long now = System.currentTimeMillis() / 1000;
        System.out.println(
        "schedule tasks using cron jobs - " + now);
    }
}
```

# 动态改写Cron
Implements `SchedulingConfigurer`就可以，想怎么改怎么改。

```java
public class ScheduleTaskSimpleJob implements SchedulingConfigurer {
    
    public void scheduleCronTask() {
    
        long now = System.currentTimeMillis() / 1000;
        System.out.println(
        "schedule tasks using cron jobs - " + now);
    }

    @Override
	public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
		taskRegistrar.addTriggerTask(new Runnable() {
			@Override
			public void run() {
				scheduleCronTask();
			}
		}, new Trigger() {
			@Override
			public Date nextExecutionTime(TriggerContext triggerContext) {
				//TODO 将时间配置10：15转换为cron
				String cron = "0 15 10 * * ?";       
				CronTrigger trigger = new CronTrigger(cron);
				
				Date nextExecDate = trigger.nextExecutionTime(triggerContext);
				return nextExecDate;
			}
		});
		
	}
}
```
