log4js-node是log4js的Node.js版本。

log4js-node的使用比较简单，以下内容主要来自官方文档。

https://github.com/log4js-node/log4js-node

## Installation

```bash
npm install log4js
```

## Usage
注意：log4js默认category的level是OFF，所以以下程序不会有输出。

```javascript
var log4js = require('log4js');
var logger = log4js.getLogger();
logger.level = 'debug';
logger.debug("Some debug messages");
```
以下程序将default category的level改为error。

```javascript
const log4js = require('log4js');
log4js.configure({
  appenders: { cheese: { type: 'file', filename: 'cheese.log' } },
  categories: { default: { appenders: ['cheese'], level: 'error' } }
});

const logger = log4js.getLogger('cheese');
logger.trace('Entering cheese testing');
logger.debug('Got cheese.');
logger.info('Cheese is Comté.');
logger.warn('Cheese is quite smelly.');
logger.error('Cheese is too ripe!');
logger.fatal('Cheese was breeding ground for listeria.');
```
成功输出error以上级别的log。

```bash
[2010-01-17 11:43:37.987] [ERROR] cheese - Cheese is too ripe!
[2010-01-17 11:43:37.990] [FATAL] cheese - Cheese was breeding ground for listeria.
```

## Example
https://github.com/log4js-node/log4js-example

### 1. log4js.configure()
configure可以接收一个JSON文件（log4js.json）作为参数。

### 2. log4js.json
定义了3种category、4种appender。其中errors是logLevelFilter，输出到errorFile，就是所有error信息会单独输出到errors.log文件中。

```json
{
    "appenders": {
      "access": {
        "type": "dateFile",
        "filename": "log/access.log",
        "pattern": "-yyyy-MM-dd",
        "category": "http"
      },
      "app": {
        "type": "file",
        "filename": "log/app.log",
        "maxLogSize": 10485760,
        "numBackups": 3
      },
      "errorFile": {
        "type": "file",
        "filename": "log/errors.log"
      },
      "errors": {
        "type": "logLevelFilter",
        "level": "ERROR",
        "appender": "errorFile"
      }
    },
    "categories": {
      "default": { "appenders": [ "app", "errors" ], "level": "DEBUG" },
      "http": { "appenders": [ "access"], "level": "DEBUG" }
    }
  }
```
### 3. log4js调用
根据category决定输出文件，getLogger('http')输出到access.log，其他情况下输出到app.log（因为category非http即default），error自动输出到errors.log文件。
```
var log4js = require('log4js');
var log = log4js.getLogger("app");

app.use(log4js.connectLogger(log4js.getLogger("http"), { level: 'auto' }));

log.error("Something went wrong:", err);
```

## 动态配置
### 1. 不同的log4js.json
因为log4js.configure支持json文件作为参数，可以为Development和Production定义不同的配置文件。   
如配置文件放在config目录下，区分dev和prod。

config/dev/log4js.json   
config/prod/log4js.json

### 2. 调用方法
根据ENV值选择调用的配置文件，即运行前set ENV=prod，default是dev。
```javascript
let env = process.env.ENV || 'dev';
let logConfigPath = './config/' + env + '/log4js.json';
let logConfig = require(logConfigPath);
log4js.configure(logConfig);
```