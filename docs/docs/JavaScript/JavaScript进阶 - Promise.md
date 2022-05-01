
JavaScript进阶 - Promise
===
Promise，中文即承诺，Promise承诺的是，未来将会按照指定的顺序执行已定义的异步操作。

Promise实质上是一个代表异步操作最终完成或失败的对象。它主要通过维护程序的内部状态来实现对流程的控制。

# Promise的三种状态
Promise只能处于以下三种状态：
* fulfilled
* rejected
* pending

当操作执行成功时，调用resolve函数将promise状态改为fulfilled，失败时，调用reject函数将promise状态改为rejected。   
程序正在运行时，状态为pending，当抛出异常，同样返回rejected。

Promise定义语法如下，支持Promise的方法必须return一个Promise对象。
```
new Promise( function(resolve, reject) {...} /* executor */  );
```

# Promise的三个方法
* then
* catch
* finally

以上三个方法都会返回一个新的Promise，所以Promise支持链式调用。

多次调用then，Promise会确保前面的异步操作完成之后再执行后面的操作，按插入顺序独立运行。

Promise链式调用里，一个catch即可捕获Promise所有代码块里的异常。

Promise运行完之后要调用的代码可以放在finally里，无论最终状态是成功或失败，它都会被调用到。

# Promise示例代码
```js
        const myPromise1 = function (param) {
            return new Promise((resolve, reject) => {
                console.log('myPromise1 is running');
                setTimeout(() => {
                    if (param) {
                        resolve('promise1');
                    } else {
                        reject(new Error('Oops!'));
                    }
                }, 0);
            });
        };

        const myPromise2 = function (param) {
            return new Promise((resolve, reject) => {
                console.log(`myPromise2 Param is ${param}`);
                // throw new Error('Oops!'); //5
                // reject(new Error('Oops!'));  //6
                // dummyFunc(); //7 not defined
                setTimeout(() => resolve('promise2'), 50);
            }).catch((err) => {
                console.log('catch Exception in myPromise2');
                console.log(err);
                throw new Error('Oh No!'); //8
            });
        };

        const myPromise3 = function (param) {
            setTimeout(() => {
                console.log(`myPromise3 Param is ${param}`);
                throw new Error('Oops!'); //1
            }, 450); //2
        };

        const myPromise4 = function (param) {
            return new Promise((resolve, reject) => {
                console.log(`myPromise4 Param is ${param}`);
                setTimeout(() => resolve('promise4'), 50);
            });
        };

        myPromise1(1) //4
            .then(myPromise2)
            .then(myPromise3)
            .then(myPromise4)
            .then(ret => {
                console.log(`final block return ${ret}`);
            }).catch(err => {//3
                console.log('catch Exception in the end');
                console.log(err);
            }).then(() => {
                console.log('then after catch');
            }).finally(() => myPromise4('finally')).then(() => {
                console.log('then after finally');
                done();
            });

```

# Promise嵌套

Promise嵌套的必须是正确定义的Promise方法（return Promise对象），否则异步操作的结果（次序）无法保证。

上述示例代码的运行结果如下：
```
myPromise1 is running
myPromise2 Param is promise1
myPromise4 Param is undefined
final block return promise4
then after catch
myPromise4 Param is finally
then after finally

myPromise3 Param is promise2
```
这个结果存在以下问题：

1. myPromise4并没有拿到myPromise3作为参数（undefined）
2. myPromise3并没有出现在期望的位置（而是最后）
3. myPromise3没有throw Error

因为myPromise3并不是Promise方法，而只是一个普通的异步方法。
当myPromise2执行完之后，myPromise3开始执行，同时myPromise4也开始执行，而不是等待myPromise3完成之后。
myPromise4之后的操作都按顺序执行，myPromise3则同时独自完成自身逻辑。

myPromise3没有throw Error（//1），是由于主程序在此之前就已经运行完毕退出了。

将myPromise3的timeout时间从450改为50（//2），则可成功抛出异常。

```
myPromise1 is running
myPromise2 Param is promise1
myPromise4 Param is undefined
myPromise3 Param is promise2
final block return promise4
then after catch
myPromise4 Param is finally

     Uncaught Error: Oops!
      at Timeout.setTimeout [as _onTimeout] (test\demo\promise.spec.js:33:23)

then after finally
(node:25368) UnhandledPromiseRejectionWarning: TypeError: Cannot set property 'state' of undefined
    at C:\swdtools\node-v10.8.0-win-x64\node_modules\mocha\lib\runner.js:602:20
    at done (C:\swdtools\node-v10.8.0-win-x64\node_modules\mocha\lib\runnable.js:319:5)
    at C:\swdtools\node-v10.8.0-win-x64\node_modules\mocha\lib\runnable.js:420:7
    at myPromise1.then.then.then.then.catch.then.finally.then (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:57:17)
(node:25368) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:25368) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
```

# Promise异常处理

## UnhandledPromiseRejection

假如Promise没有添加任何catch代码块，程序出错（rejected）时将会报UnhandledPromiseRejection。

开发过程中遇到此错误说明Promise相关代码可能还存在问题。

在示例中删除catch代码块（//3），将myPromise1参数改为0（//4）则重现此错误。
```
myPromise1 is running
myPromise4 Param is finally
(node:26412) UnhandledPromiseRejectionWarning: Error: Oops!
    at Timeout.setTimeout [as _onTimeout] (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:11:32)
    at ontimeout (timers.js:424:11)
    at tryOnTimeout (timers.js:288:5)
    at listOnTimeout (timers.js:251:5)
    at Timer.processTimers (timers.js:211:10)
(node:26412) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:26412) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
```

## 隐含try...catch

Promise定义（executor）里的代码无需显式添加try...catch代码块，错误会被自动捕获成一个rejection。

所以Promise里以下代码的效果是一样的。
```
// throw new Error('Oops!'); //5
// reject(new Error('Oops!'));  //6
```

## Rethrow

可以在链式调用的任何一个Promise里catch异常，进行必要的处理后重新throw出来。

启用myPromise2里的dummyFunc()（//7），运行结果如下。    
可以看到Error两次被catch，而且不再运行后面then里面的myPromise3和myPromise4（catch之后没影响）。
```
myPromise1 is running
myPromise2 Param is promise1
catch Exception in myPromise2
ReferenceError: dummyFunc is not defined
    at Promise (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:22:17)
    at new Promise (<anonymous>)
    at myPromise2 (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:18:20)
    at myPromise1.then.ret (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:46:26)
catch Exception in the end
Error: Oh No!
    at Promise.catch (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:27:23)
then after catch
myPromise4 Param is finally
then after finally
```

Comment掉`throw new Error('Oh No!'); `（//8），则结果如下。   
因为Error已经在myPromise2里catch和处理，所以后面的代码都正常运行。
```
myPromise1 is running
myPromise2 Param is promise1
catch Exception in myPromise2
ReferenceError: dummyFunc is not defined
    at Promise (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:22:17)
    at new Promise (<anonymous>)
    at myPromise2 (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:18:20)
    at myPromise1.then.ret (C:\Users\pan\workspace\nodejs\autotest-node\test\demo\promise.spec.js:46:26)
myPromise4 Param is undefined
final block return promise4
then after catch
myPromise4 Param is finally
then after finally

myPromise3 Param is undefined
```

# 怎么测试Promise

Promise方法的测试和普通方法一样，只是返回对象比较特殊。

测试的难点在于，在调用程序里，如何stub Promise方法。

sinon为Promise提供了如下支持。

测试正常执行（resolve）条件下的代码块：   
```js
sinon.stub(s, 'sendMessage').resolves('data');
```

测试catch里（reject）的代码块：
```js
sinon.stub(s, 'sendMessage').returns(Promise.reject(new Error('Oops!')));
```


