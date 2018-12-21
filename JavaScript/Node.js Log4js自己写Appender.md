Node.js Log4js写Log的同时想做点什么，可以自己写Appender
===
log4js-node集成appender用的是Listener模式， 所以可以方便地添加自定义的appender，这样就能在写log的同时做点额外的事情，比如把log发送到自己设计好的接口。

## Optional Appenders
以下是log4js-node当前提供的可选appender。
* [gelf](https://github.com/log4js-node/gelf)
* [hipchat](https://github.com/log4js-node/hipchat)
* [logFaces-HTTP](https://github.com/log4js-node/logFaces-HTTP)
* [logFaces-UDP](https://github.com/log4js-node/logFaces-UDP)
* [loggly](https://github.com/log4js-node/loggly)
* [logstashHTTP](https://github.com/log4js-node/logstashHTTP)
* [logstashUDP](https://github.com/log4js-node/logstashUDP)
* [mailgun](https://github.com/log4js-node/mailgun)
* [rabbitmq](https://github.com/log4js-node/rabbitmq)
* [redis](https://github.com/log4js-node/redis)
* [slack](https://github.com/log4js-node/slack)
* [smtp](https://github.com/log4js-node/smtp)

## Writing Appender

### My Appender
可以直接copy一个现成的appender来改，这里是copy dateFile，实现部分只是加`Process by myAppender - `前缀输出，而且只处理ERROR以上的log。

log4js-myAppender.js
```javascript
'use strict';

const os = require('os');

const eol = os.EOL || '\n';

/**
 * TODO: incomplete example.
 * @filename base filename.
 * @pattern the format that will be added to the end of filename when rolling,
 *          also used to check when to roll files - defaults to '.yyyy-MM-dd'
 * @layout layout function for log messages - defaults to basicLayout
 * @timezoneOffset optional timezone offset in minutes - defaults to system local
 */
function appender(
  filename,
  pattern,
  layout,
  options,
  timezoneOffset
) {
  const app = function (logEvent) {
    if (logEvent.level.isGreaterThanOrEqualTo('ERROR')){
      console.log('Process by myAppender - ' + layout(logEvent, timezoneOffset) + eol);
    }

    // console.log(config.level);
  };

  app.shutdown = function (complete) {
    // complete();
  };

  return app;
}

function configure(config, layouts) {
  let layout = layouts.basicLayout;

  if (config.layout) {
    layout = layouts.layout(config.layout.type, config.layout);
  }

  if (!config.alwaysIncludePattern) {
    config.alwaysIncludePattern = false;
  }

  return appender(
    config.filename,
    config.pattern,
    layout,
    config,
    config.timezoneOffset
  );
}

module.exports.configure = configure;

```
### log4js.configure
`type`填写对应appender相对于项目根目录的路径，其他参数此例只用到`level`。
```json
        "errors": {
            "type": './demo/log4js-myAppender',
            'level': 'ERROR'
        }
```

### Appender Type
需要小心的是插件的加载机制。  
Log4js configure里appender type需要填写相对于project root的路径。

已有的可选插件路径不需要这样写是因为作为独立module发布了。

具体加载顺序如下：

1. The core appenders: `require('./appenders/' + type)`
2. node_modules: `require(type)`
3. relative to the main file of your application: `require(path.dirname(require.main.filename) + '/' + type)`
4. relative to the process' current working directory: `require(process.cwd() + '/' + type)`

## 参考
https://github.com/log4js-node/log4js-node/blob/master/docs/writing-appenders.md
