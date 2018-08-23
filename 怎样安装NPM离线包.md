怎样安装NPM离线包
======
因为一些（你懂的）原因，工作环境无法直接使用`npm install`联网安装npm包，稍微花了点时间研究了一下，Mark下来，有机会看源码再补充。

## 最佳方案
别浪费时间了。   
最好还是在网络环境下把所需的包全部安装好，再想办法搬回来。   
尽管可以一个一个下载包，但是其中依赖关系却错综复杂，对于关系复杂的情况，逐个下载基本上不可行。

## 可行办法
假设没有依赖关系，则可以下载安装包，然后放到node_modules。注意文件夹名称一般要删掉版本号，才与package.json描述一致。

或者直接指向压缩包运行install命令。   
`npm install <tarball file>`

这种方法对于有依赖关系的包不可行，就算已经把所有依赖包放到该安装包里的node_modules目录下，安装过程还是会去尝试连接到网络。

如下方法却可行，但却只是使用symlink方式连接到目标文件夹。
`npm install <folder>`

看了一下help，并不是bug，但总感觉不太友好。
```
Install the package in the directory as a symlink in the current project. Its dependencies will be installed before it's linked. If <folder> sits inside the root of your project, its dependencies may be hoisted to the toplevel node_modules as they would for other types of dependencies.
```

### 一定要npm install？
不是放到node_modules下就可以？为什么还要npm install？   
除了更新package.json，刚好我用来试的是express-generator。如果只是放到<nodejs_root>/node_modules文件夹下，express命令行不可用。   
npm install后，<nodejs_root>下出现express和express.cmd，命令可用。  

所以对于这种要添加命令行工具的包，需要用npm install来安装，比如：exress-generator、TypeScript。

