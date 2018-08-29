发现ThreadPoolExecuter的行为模式跟自己之前的理解有些出入（坑），内在逻辑并不是表面上看那么直观，特地记录一下。

## ThreadPoolExecutor构造函数
```Java
    /**
     * Creates a new {@code ThreadPoolExecutor} with the given initial
     * parameters.
     *
     * @param corePoolSize the number of threads to keep in the pool, even
     *        if they are idle, unless {@code allowCoreThreadTimeOut} is set
     * @param maximumPoolSize the maximum number of threads to allow in the
     *        pool
     * @param keepAliveTime when the number of threads is greater than
     *        the core, this is the maximum time that excess idle threads
     *        will wait for new tasks before terminating.
     * @param unit the time unit for the {@code keepAliveTime} argument
     * @param workQueue the queue to use for holding tasks before they are
     *        executed.  This queue will hold only the {@code Runnable}
     *        tasks submitted by the {@code execute} method.
     * @param threadFactory the factory to use when the executor
     *        creates a new thread
     * @param handler the handler to use when execution is blocked
     *        because the thread bounds and queue capacities are reached
     * @throws IllegalArgumentException if one of the following holds:<br>
     *         {@code corePoolSize < 0}<br>
     *         {@code keepAliveTime < 0}<br>
     *         {@code maximumPoolSize <= 0}<br>
     *         {@code maximumPoolSize < corePoolSize}
     * @throws NullPointerException if {@code workQueue}
     *         or {@code threadFactory} or {@code handler} is null
     */
    public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue,
                              ThreadFactory threadFactory,
                              RejectedExecutionHandler handler) {
        if (corePoolSize < 0 ||
            maximumPoolSize <= 0 ||
            maximumPoolSize < corePoolSize ||
            keepAliveTime < 0)
            throw new IllegalArgumentException();
        if (workQueue == null || threadFactory == null || handler == null)
            throw new NullPointerException();
        this.acc = System.getSecurityManager() == null ?
                null :
                AccessController.getContext();
        this.corePoolSize = corePoolSize;
        this.maximumPoolSize = maximumPoolSize;
        this.workQueue = workQueue;
        this.keepAliveTime = unit.toNanos(keepAliveTime);
        this.threadFactory = threadFactory;
        this.handler = handler;
    }
```

也可使用缺省的`ThreadFactory`或`RejectedExecutionHandler`，通过其他构造函数，如：

```Java
    public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue) {
        this(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue,
             Executors.defaultThreadFactory(), defaultHandler);
    }
```

## ThreadPoolExecutor参数说明
* corePoolSize

线程池核心线程数，即使处于闲置状态也不会回收，除非将`allowCoreThreadTimeOut`设置为`true`。

* maximumPoolSize

线程池所能容纳的最大线程数。

* keepAliveTime

当线程数超过核心线程数时，这些非核心线程闲置超过`keepAliveTime`就会被回收。

* unit

`keepAliveTime`的时间单位，如`TimeUnit.SECONDS`。

* workQueue

工作队列，保存通过`execute`方法提交的还没有执行的`Runnable`任务。

* threadFactory

创建线程的工厂类，可以按需重写，默认的工厂类如下：
```Java
    /**
     * The default thread factory
     */
    static class DefaultThreadFactory implements ThreadFactory {
        private static final AtomicInteger poolNumber = new AtomicInteger(1);
        private final ThreadGroup group;
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        private final String namePrefix;

        DefaultThreadFactory() {
            SecurityManager s = System.getSecurityManager();
            group = (s != null) ? s.getThreadGroup() :
                                  Thread.currentThread().getThreadGroup();
            namePrefix = "pool-" +
                          poolNumber.getAndIncrement() +
                         "-thread-";
        }

        public Thread newThread(Runnable r) {
            Thread t = new Thread(group, r,
                                  namePrefix + threadNumber.getAndIncrement(),
                                  0);
            if (t.isDaemon())
                t.setDaemon(false);
            if (t.getPriority() != Thread.NORM_PRIORITY)
                t.setPriority(Thread.NORM_PRIORITY);
            return t;
        }
    }
```

* handler

`RejectedExecutionHandler`是用来定义线程资源耗尽时的拒绝处理策略，缺省是`AbortPolicy`，抛出拒绝处理异常。
线程池的使用应该要能满足业务的需求，从这个意义上来说，抛出异常是合适的。遇到此异常应该首先回去检视线程池的参数定义而非改变策略。
```Java
    /**
     * A handler for rejected tasks that throws a
     * {@code RejectedExecutionException}.
     */
    public static class AbortPolicy implements RejectedExecutionHandler {
        /**
         * Creates an {@code AbortPolicy}.
         */
        public AbortPolicy() { }

        /**
         * Always throws RejectedExecutionException.
         *
         * @param r the runnable task requested to be executed
         * @param e the executor attempting to execute this task
         * @throws RejectedExecutionException always
         */
        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            throw new RejectedExecutionException("Task " + r.toString() +
                                                 " rejected from " +
                                                 e.toString());
        }
    }
```

## ThreadPoolExecutor行为模式
* 1.`线程数 <= corePoolSize`，新建一个核心线程执行任务
* 2.`corePoolSize < 线程数 <= maximumPoolSize`，将任务移入队列等待
* 3.如果队列已满，则新建非核心线程执行任务
* 4.队列已满，且`线程数 > maximumPoolSize`，则由`RejectedExecutionHandler`抛出异常

所以：   
`线程池的最大运行线程数 = 核心线程数 + 非核心线程数`   
`线程池的任务吞吐量 = 最大运行线程数 + 任务队列容量`。   

ThreadPoolExecutor的行为模式与所使用的BlockingQueue有很大关系。当使用SynchronousQueue时，任务队列容量为0，如果`线程数 > corePoolSize`，直接新建非核心线程执行后续任务，直到超过`maximumPoolSize`抛出异常。   
当使用没有大小限制的`LinkedBlockingDeque`时，任务队列容量无限，`maximumPoolSize`限制失去意义，任何时候最多只有`corePoolSize`个线程正在运行，新任务可以持续添加到任务队列中等待。

## ThreadPoolExecutor验证实例
```
package pan.rufeng.demo;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class DemoThreadPoolExecuter {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Test begin");
        Runnable myRunnable = new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(2000);
//                    System.out.println(Thread.currentThread().getName() + " run");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            }
        };

        // Test case 1: SynchronousQueue, 6 tasks, corePoolSize 3, maxmumPoolSize 6, keepAliveTime 5秒
        // keepAliveTime to 6
        // maxmumPoolSize to 5
        // Test case 2: LinkedBlockingQueue without size limit, 6 tasks, corePoolSize 4, maxmumPoolSize 6, keepAliveTime 5秒
        // Test case 3: ArrayBlockingQueue或LinkedBlockingQueue with size limit, 6 tasks, corePoolSize 4, maxmumPoolSize 6, keepAliveTime 5秒
        ThreadPoolExecutor tpe = new ThreadPoolExecutor(3, 6, 5, TimeUnit.SECONDS, new LinkedBlockingQueue<Runnable>(2));
        executeRunnable3Times("第一次提交：", myRunnable, tpe);
        executeRunnable3Times("第二次提交：",myRunnable, tpe);
        Thread.sleep(8000);
        System.out.println("   8秒之后：corePoolSize: " + tpe.getCorePoolSize() + "\t poolSize: " + tpe.getPoolSize() + "\t queueSize: " + tpe.getQueue().size());

    }

    private static void executeRunnable3Times(String title, Runnable myRunnable, ThreadPoolExecutor tpe) {
        tpe.execute(myRunnable);
        tpe.execute(myRunnable);
        tpe.execute(myRunnable);
        System.out.println(title + "corePoolSize: " + tpe.getCorePoolSize() + "\t poolSize: " + tpe.getPoolSize() + "\t queueSize: " + tpe.getQueue().size());
    }
}

```
总共提交6个任务，每个任务睡眠2秒，分两次提交，每次提交3个任务，提交之后打印Executor状况，主线程等待8秒之后再一次打印Executor最终状态（验证线程回收）。   

* Test case 1: SynchronousQueue, 6 tasks, corePoolSize 4, maxmumPoolSize 6, keepAliveTime 5
```
ThreadPoolExecutor tpe = new ThreadPoolExecutor(4, 6, 5, TimeUnit.SECONDS, new SynchronousQueue<Runnable>());
```
结果：第二次提交超过corePoolSize后，创建2个非核心线程执行，没有任务放进等待队列。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 4	 poolSize: 6	 queueSize: 0
   8秒之后：corePoolSize: 4	 poolSize: 4	 queueSize: 0
```
keepAliveTime从5秒改成6秒，或者主线程等待时间8秒调到7秒，则非核心线程不回收。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 4	 poolSize: 6	 queueSize: 0
   8秒之后：corePoolSize: 4	 poolSize: 6	 queueSize: 0
```
提交线程数（6）大于maxmumPoolSize（如改成5），则throw RejectedExecutionException。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
Exception in thread "main" java.util.concurrent.RejectedExecutionException: Task pan.rufeng.demo.DemoThreadPoolExecuter$1@45ee12a7 rejected from java.util.concurrent.ThreadPoolExecutor@330bedb4[Running, pool size = 5, active threads = 5, queued tasks = 0, completed tasks = 0]
	at java.util.concurrent.ThreadPoolExecutor$AbortPolicy.rejectedExecution(ThreadPoolExecutor.java:2063)
	at java.util.concurrent.ThreadPoolExecutor.reject(ThreadPoolExecutor.java:830)
	at java.util.concurrent.ThreadPoolExecutor.execute(ThreadPoolExecutor.java:1379)
	at pan.rufeng.demo.DemoThreadPoolExecuter.executeRunnable3Times(DemoThreadPoolExecuter.java:36)
	at pan.rufeng.demo.DemoThreadPoolExecuter.main(DemoThreadPoolExecuter.java:27)
```
* Test case 2: LinkedBlockingQueue without size limit, 6 tasks, corePoolSize 4, maxmumPoolSize 6, keepAliveTime 5秒
```
ThreadPoolExecutor tpe = new ThreadPoolExecutor(4, 6, 5, TimeUnit.SECONDS, new LinkedBlockingQueue<Runnable>());
```
结果：第二次提交之后，2个任务放到队列等待。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 4	 poolSize: 4	 queueSize: 2
   8秒之后：corePoolSize: 4	 poolSize: 4	 queueSize: 0
```
keepAliveTime改到8秒或者更大，对结果没影响，因为这里只用到核心线程。   
maxmumPoolSize（如改成4）小于提交线程数（6），程序依然正常执行，结果同上。maxmumPoolSize限制失去意义（但不能小于corePoolSize）。   

* Test case 3: ArrayBlockingQueue或LinkedBlockingQueue with size limit, 6 tasks, corePoolSize 4, maxmumPoolSize 6, keepAliveTime 5秒
```
ThreadPoolExecutor tpe = new ThreadPoolExecutor(4, 6, 5, TimeUnit.SECONDS, new LinkedBlockingQueue<Runnable>(1));
ThreadPoolExecutor tpe = new ThreadPoolExecutor(4, 6, 5, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(1));
```
结果：第二次提交超过corePoolSize后，创建1个非核心线程执行，1个任务放进等待队列。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 4	 poolSize: 5	 queueSize: 1
   8秒之后：corePoolSize: 4	 poolSize: 4	 queueSize: 0
```
keepAliveTime从5秒改成6秒，或者主线程等待时间8秒调到7秒，则非核心线程不回收。
```
第一次提交：corePoolSize: 4	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 4	 poolSize: 5	 queueSize: 1
   8秒之后：corePoolSize: 4	 poolSize: 5	 queueSize: 0
```
可见，线程池的最大运行线程数为5，maxmumPoolSize设置需大于5，否则throw RejectedExecutionException。  
将corePoolSize设为3，队列容量设为2，则可得如下结果。第二次提交任务时，创建1个非核心线程执行，剩下的2个任务进队列。
```
第一次提交：corePoolSize: 3	 poolSize: 3	 queueSize: 0
第二次提交：corePoolSize: 3	 poolSize: 4	 queueSize: 2
   8秒之后：corePoolSize: 3	 poolSize: 3	 queueSize: 0
```

具体验证例子也可参考：
[https://blog.csdn.net/qq_25806863/article/details/71126867](https://blog.csdn.net/qq_25806863/article/details/71126867)

Java Doc:     
[https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ThreadPoolExecutor.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ThreadPoolExecutor.html)

阅读导航：

[toc]