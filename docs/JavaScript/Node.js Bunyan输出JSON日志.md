Node.js Bunyan输出JSON日志
===
日志应该是结构化的，处理日志的主要应该是机器而不是人，这就是日志输出为JSON的好处，而Bunyan即是一个简单快速的JSON日志库。

正式Demo可参考Github：     
https://github.com/prufeng/autotest-node/tree/master/demo

# Install
```
npm install bunyan
```

# Helloworld
## 测试代码
```javascript
//app.js
var bunyan = require('bunyan');
var log = bunyan.createLogger({name:'app'});
log.info('hello world');
log.warn({key: 'test'}, 'hello world');
log.error('hello world');
```
## 输出JSON
```bash
{"name":"app","hostname":"PC70358896","pid":12248,"level":30,"msg":"hello world","time":"2018-11-26T09:31:46.657Z","v":0}
{"name":"app","hostname":"PC70358896","pid":12248,"level":40,"key":"test","msg":"hello world","time":"2018-11-26T09:31:46.659Z","v":0}
{"name":"app","hostname":"PC70358896","pid":12248,"level":50,"msg":"hello world","time":"2018-11-26T09:31:46.659Z","v":0}
```

## 输出到文件
```javascript
var log2file = bunyan.createLogger({
  name: 'log2file',
  streams:[{
    // type: 'file', //default type
    path: './logs/bunyan.log',
  }]
});
log2file.info('hello world');
log2file.warn({key: 'test'}, 'hello world');
log2file.error('hello world');
```

## 输出到轮转文件
可定义多个Stream，rotating-file昨天的log自动加后缀.0，前天加后缀.1，以此类推。

另外，测试过程中发现要事先建立logs文件夹，否则会fail。

```javascript
var log2file = bunyan.createLogger({
  name: 'log2file',
  streams:[{
    // type: 'file',  //default type
    path: './logs/bunyan.log',
  },
  {
    type: 'rotating-file',
    path: './logs/bunyan-rf.log',
    period: '1d', //daily rotation
    count: 3  //keep 3 backup
  },
  {
    type: 'rotating-file',
    level: 'error', //error log, default info
    path: './logs/bunyan-rf-error.log',
    period: '1d',
    count: 3
  }]
});
log2file.info('hello world');
log2file.warn({key: 'test'}, 'hello world');
log2file.error('hello world');

```

# express-bunyan-logger
## Install
```
npm i express-bunyan-logger
```

## 测试代码
```javascript
//app.js
app.use(require('express-bunyan-logger')(express));

var express = {
    name: 'bunyan-express',
    // format: ":remote-address - :user-agent[major] custom logger",
    streams: [
        {
            type: 'rotating-file',
            path: './logs/bunyan-rf-express.log',
            period: '1d',
            count: 3
        }
    ]
};
```

## 输出
```bash
{"name":"bunyan-express","hostname":"PC70358896","pid":16780,"req_id":"5fe2acbb-7441-4480-929d-c54351424ead","level":40,"remote-address":"::ffff:127.0.0.1","ip":"::ffff:127.0.0.1","method":"GET","url":"/wrongUrl","referer":"-","user-agent":{"family":"Other","major":"0","minor":"0","patch":"0","device":{"family":"Other","major":"0","minor":"0","patch":"0"},"os":{"family":"Other","major":"0","minor":"0","patch":"0"}},"body":{},"short-body":"{}","http-version":"1.1","response-time":11.590723,"response-hrtime":[0,11590723],"status-code":404,"req-headers":{"host":"127.0.0.1:54929","accept-encoding":"gzip, deflate","user-agent":"node-superagent/3.8.3","connection":"close"},"res-headers":{"x-powered-by":"Express","content-type":"text/html; charset=utf-8","content-length":"2483","etag":"W/\"9b3-3MaH2Djfdd7bcNOKTO1QCw+mCBs\""},"req":{"method":"GET","url":"/wrongUrl","headers":{"host":"127.0.0.1:54929","accept-encoding":"gzip, deflate","user-agent":"node-superagent/3.8.3","connection":"close"},"remoteAddress":"::ffff:127.0.0.1","remotePort":54930},"res":{"statusCode":404,"header":"HTTP/1.1 404 Not Found\r\nX-Powered-By: Express\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 2483\r\nETag: W/\"9b3-3MaH2Djfdd7bcNOKTO1QCw+mCBs\"\r\nDate: Tue, 27 Nov 2018 07:49:47 GMT\r\nConnection: close\r\n\r\n"},"incoming":"<--","msg":"::ffff:127.0.0.1 - 0","time":"2018-11-27T07:49:47.582Z","v":0}
```
# 参考
https://github.com/trentm/node-bunyan   
https://github.com/villadora/express-bunyan-logger    
https://medium.com/@bansalnagesh/better-logging-with-bunyan-eff940d29956
