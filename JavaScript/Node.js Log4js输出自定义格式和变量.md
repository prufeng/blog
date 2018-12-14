Node.js Log4js输出自定义格式和变量
===
Log4js输出自定义格式，或者想在log里添加自己定义的变量，如显示当前用户名，可以通过pattern layout来实现。

# Log4js Pattern Layout
* 设置占位符如`%X{user}`
* 在代码里调用`addContext('user','userName')`更新变量

```javascript
log4js.configure({
  appenders: {
    out: { type: 'stdout', layout: {
      type: 'pattern',
      pattern: '%d %p %c %X{user} %m%n'
    }}
  },
  categories: { default: { appenders: ['out'], level: 'info' } }
});
const logger = log4js.getLogger();
logger.addContext('user', 'charlie');
logger.info('doing something.');
```

This would output:

```
2017-06-01 08:32:56.283 INFO default charlie doing something.
```

# 如何优雅地addContext
思路是利用express middleware，截取request获得参数信息，调用addContext()设置到log4js后，再转发到router的其他请求。这样，在该router里的所有logger都可以格式化地print出我们定义的参数。

这里有个简单Demo，其他AOP方法尚待研究。    
https://github.com/prufeng/autotest-node

# 参考
https://github.com/log4js-node/log4js-node/blob/master/docs/layouts.md