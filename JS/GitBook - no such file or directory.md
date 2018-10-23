换一台电脑打开GitBook项目居然有错。

Error: ENOENT: no such file or directory, stat 'C:\***demo_book\\_book\gitbook\gitbook-plugin-fontsettings\fontsettings.js'

原来是一个Bug（Vesion：3.2.3）。

https://github.com/GitbookIO/gitbook/issues/1309

解决办法如下。

用户目录下找到以下文件。
\<user>\\.gitbook\versions\3.2.3\lib\output\website\copyPluginAssets.js

Replace all   
`confirm: true`   
with   
`confirm: false`



