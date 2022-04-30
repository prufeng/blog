
Angular Karma - Chrome have not captured in 60000 ms
===
给Google带偏了，各种改config各种试，花了大半天，给大家提供个思路。   

这个错的root cause是Chrome启动不了。

为什么启动不了?   
首先看下Chrome存不存在正不正常能不能启动！   
Command line试一下。

我的情况是本机可以，运维机器不行，缺少相应权限，却又悲剧地默认运维机器的Chrome没问题！所以总以为问题出在其他地方！

开Debug可以看到Chrome启动的command line。首先检查下路径对不对。
```
20-Mar-2019 01:32:56  20 03 2019 01:32:56.381:INFO [karma]: Karma v1.7.1 server started at http://0.0.0.0:9876/ 
20-Mar-2019 01:32:56  20 03 2019 01:32:56.381:INFO [launcher]: Launching browser ChromeHeadless with unlimited concurrency 
20-Mar-2019 01:32:56  20 03 2019 01:32:56.491:INFO [launcher]: Starting browser ChromeHeadless 
20-Mar-2019 01:32:56  20 03 2019 01:32:56.492:DEBUG [temp-dir]: Creating temp dir at C:\Windows\TEMP\karma-98458715 
20-Mar-2019 01:32:56  20 03 2019 01:32:56.493:DEBUG [launcher]: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --user-data-dir=C:\Windows\TEMP\karma-98458715 --no-default-browser-check --no-first-run --disable-default-apps --disable-popup-blocking --disable-translate --disable-background-timer-throttling --disable-renderer-backgrounding --disable-device-discovery-notifications http://localhost:9876/?id=98458715 --headless --disable-gpu --remote-debugging-port=9222 
20-Mar-2019 01:34:56  20 03 2019 01:34:56.511:WARN [launcher]: ChromeHeadless have not captured in 120000 ms, killing. 
20-Mar-2019 01:34:58  20 03 2019 01:34:58.526:WARN [launcher]: ChromeHeadless was not killed in 2000 ms, sending SIGKILL. 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.542:WARN [launcher]: ChromeHeadless was not killed by SIGKILL in 2000 ms, continuing. 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.542:DEBUG [launcher]: Process ChromeHeadless exited with code -1 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.543:DEBUG [temp-dir]: Cleaning temp dir C:\Windows\TEMP\karma-98458715 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.547:DEBUG [launcher]: ChromeHeadless failed (timeout). Not restarting. 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.550:DEBUG [karma]: Run complete, exiting. 
20-Mar-2019 01:35:00  20 03 2019 01:35:00.551:DEBUG [launcher]: Disconnecting all browsers 
20-Mar-2019 01:35:00  npm ERR! Test failed.  See above for more details. 

```
Debug这样开。

karma.conf.js
```
logLevel: config.LOG_DEBUG,
```

可以这样加大启动时间：`captureTimeout:120000`（default 60000）。

另外，`browsers: ['Chrome']`和`browsers: ['ChromeHeadless']`的区别是：ChromeHeadless是无弹窗模式。

自定义Browser，要注意自定义的名称是否对应（ChromeHeadless_test）。
```js
browsers: ['ChromeHeadless_test'],
    customLaunchers: {
      ChromeHeadless_test: {
        base: 'ChromeHeadless',
        flags: [
          '--disable-extensions', 
          '--no-sandbox', 
          '--disable-web-security', 
          '--no-proxy-server']
      }
    },

```
实际测试中剪掉一些feature会快两三秒，如非必要还是用默认就好，不喜弹窗可用`browsers: ['ChromeHeadless']`。

其他问题可以直接看launcher源代码，可能还快过Google，比较简单。

https://github.com/karma-runner/karma-chrome-launcher
