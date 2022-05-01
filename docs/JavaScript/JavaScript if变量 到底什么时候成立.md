 
 JavaScript if(变量) 到底什么时候成立
 ===
JavaScript实在是神通广大，虽然写了很多年，一些简单的代码有时写着写着还是忍不住会怀疑。

比如if(variable) 这样的语句到底什么时候成立，具体是怎么判断的？

今天忍不住再来测试一下。

# 结论

#### 返回false的变量值：

* false
* 0
* 空字符串
* undefined
* null
* NaN

#### 返回true的变量值：

* true 
* 1
* 非空字符串
* 对象
* 数组

非空字符串包括空格（`' '`），`'false'`，`'0'`。

空对象和空数组都返回true。

# 测试代码
 ```js
        let count = 0;
        let func = (tt) => {
            count++;
            if (tt) {
                console.log(count + '. ' + tt + ' is true');
            } else {
                console.log(count + '. ' + tt + ' is false');
            }
        };

        let tt;
        func(tt);
        tt = 1;
        func(tt);
        tt = 0;
        func(tt);
        tt = true;
        func(tt);
        tt = false;
        func(tt);
        tt = 'true';
        func(tt);
        tt = 'false';
        func(tt);
        tt = '0';
        func(tt);
        tt = '';
        func(tt);
        tt = ' ';
        func(tt);
        tt = null;
        func(tt);
        tt = NaN;
        func(tt);
        tt = {};
        func(tt);
        tt = [];
        func(tt);
```
# 输出结果

```bash
1. undefined is false
2. 1 is true
3. 0 is false
4. true is true
5. false is false
6. true is true
7. false is true
8.  is false
9.   is true
10. null is false
11. NaN is false
12. [object Object] is true
13.  is true
```

# 其他逻辑运算

From: [w3cshool](http://www.w3school.com.cn/js/pro_js_operators_boolean.asp)

## NOT
与逻辑 OR 和逻辑 AND 运算符不同的是，逻辑 NOT 运算符返回的一定是 Boolean 值。

逻辑 NOT 运算符的行为如下：

* 如果运算数是对象，返回 false
* 如果运算数是数字 0，返回 true
* 如果运算数是 0 以外的任何数字，返回 false
* 如果运算数是 null，返回 true
* 如果运算数是 NaN，返回 true
* 如果运算数是 undefined，发生错误

## AND
逻辑 AND 运算的运算数可以是任何类型的，不止是 Boolean 值。

如果某个运算数不是原始的 Boolean 型值，逻辑 AND 运算并不一定返回 Boolean 值：

* 如果一个运算数是对象，另一个是 Boolean 值，返回该对象。
* 如果两个运算数都是对象，返回第二个对象。
* 如果某个运算数是 null，返回 null。
* 如果某个运算数是 NaN，返回 NaN。
* 如果某个运算数是 undefined，发生错误。

## OR
与逻辑 AND 运算符相似，如果某个运算数不是 Boolean 值，逻辑 OR 运算并不一定返回 Boolean 值：

* 如果一个运算数是对象，并且该对象左边的运算数值均为 false，则返回该对象。
* 如果两个运算数都是对象，返回第一个对象。
* 如果最后一个运算数是 null，并且其他运算数值均为 false，则返回 null。
* 如果最后一个运算数是 NaN，并且其他运算数值均为 false，则返回 NaN。
* 如果某个运算数是 undefined，发生错误。
