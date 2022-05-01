Node.js Log4js输出JSON日志
===
# Log4js Json Layout
### 代码：

```javascript
const log4js = require('log4js');

log4js.addLayout('json', function(config) {
  return function(logEvent) { return JSON.stringify(logEvent) + config.separator; }
});

log4js.configure({
  appenders: {
    out: { type: 'stdout', layout: { type: 'json', separator: ',' } }
  },
  categories: {
    default: { appenders: ['out'], level: 'info' }
  }
});

const logger = log4js.getLogger('json-test');
logger.info('this is just a test');
logger.error('of a custom appender');
logger.warn('that outputs json');
log4js.shutdown(() => {});
```
### 输出:

```bash
{"startTime":"2017-06-05T22:23:08.479Z","categoryName":"json-test","data":["this is just a test"],"level":{"level":20000,"levelStr":"INFO"},"context":{}},
{"startTime":"2017-06-05T22:23:08.483Z","categoryName":"json-test","data":["of a custom appender"],"level":{"level":40000,"levelStr":"ERROR"},"context":{}},
{"startTime":"2017-06-05T22:23:08.483Z","categoryName":"json-test","data":["that outputs json"],"level":{"level":30000,"levelStr":"WARN"},"context":{}},
```

# Issue
发现`startTime`的时间格式与普通layout不一致，输出的并不是local时间。GitHub上给他们提了一个Issue。

https://github.com/log4js-node/log4js-node/issues/814

# 参考
https://github.com/log4js-node/log4js-node/blob/master/docs/layouts.md