npm run传递参数
＝＝＝

karma.conf.js使用以下设置时，unit test会不停地跑。
```
autoWatch: false,
singleRun: true,
```

想只跑一次，发现命令行参数不起效果。
```
npm run ng test --watch=false --code-coverage
```
原来需要加`--`，这是npm传递参数给script的方法。
```
npm run ng test -- --watch=false --code-coverage
```

`npm help run`查看详细说明。
>As of npm@2.0.0, you can use custom arguments when executing scripts. The special option -- is used by getopt to delimit the end of the options. npm will pass all the arguments after the -- directly to your script:

>npm run test -- --grep="pattern"

>The arguments will only be passed to the script specified after npm run and not to any pre or post script.


不过不应该整天打这么长的命令行，复杂的命令都应该放到script里。

package.json
```
"test": "ng test --watch=false --code-coverage",
```
然后`npm test`就可以。
