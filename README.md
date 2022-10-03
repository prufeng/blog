Rufeng's Blog
======
All non-project logs, or blog articles.

# CSDN
https://blog.csdn.net/prufeng

# 非技术公众号
好辣K（haolakei）

# Gitbook 

## MD to HTML
```
# Generate SUMMARY again to see if any update
> update.bat


$ node -v
v16.13.1

$ npm i -g gitbook-cli
# Fix polyfills.js:287 issue, comment out statFix()

$ gitbook -V
CLI version: 2.3.2
GitBook version: 3.2.3

# Add book.json for expandable-chapters plugins
gitbook install

# Static html menu not work
# Fix issue in _book/gitbook/theme.js, 'if(m)' -> 'if(false)', build again will replace
# Remove '()' in MD file name 

gitbook serve

http://localhost:4000/

```

## To Pdf
Install https://calibre-ebook.com/download_windows64

Set ebook-convert to system path: `C:\Program Files\Calibre2`

```
gitbook pdf
```
