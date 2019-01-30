Node.js Sinon测试替身
===
# 测试替身
测试替身(Test Double)，顾名思义，即测试时用来代替系统中某一部分的模拟技术的统称。

## 测试替身的作用
* 隔离被测代码
* 加速执行测试
* 使执行变得确定
* 模拟特殊情况
* 访问隐藏信息

上述列表copy from：https://yq.aliyun.com/articles/118887


## 测试替身的类型
* Dummy objects are passed around but never actually used. Usually they are just used to fill parameter lists.

* Fake objects actually have working implementations, but usually take some shortcut which makes them not suitable for production (an in memory database is a good example).

* Stubs provide canned answers to calls made during the test, usually not responding at all to anything outside what's programmed in for the test.

* Spies are stubs that also record some information based on how they were called. One form of this might be an email service that records how many messages it was sent.

* Mocks are what we are talking about here: objects pre-programmed with expectations which form a specification of the calls they are expected to receive.

上述分类copy from大神blog：   
https://martinfowler.com/articles/mocksArentStubs.html

# Sinon单元测试替身
Node.js的单元测试替身技术，Sinon应该是主流，下面结合实例分析理解下。

例子主要来源于《JavaScript测试驱动开发》，不过书里的Sinon版本已经过时了，无法运行，所以这里是改进版。也用到Mocha和Chai。

https://github.com/prufeng/autotest-node/blob/master/test/pam/stockfetch.spec.js

```javascript
    it('read should invoke error handler for invalid file', function (done) {
        var onError = function (err) {
            expect(err).to.be.eql('Error reading file: dummyInvalidFile');
            done();
        };
        var stub = sinon.stub(fs, 'readFile');
        stub.yields(new Error('Failed to read file'));
        
        stockFetch.readTickerFile('dummyInvalidFile', onError);
        stub.restore();
    });
    
    it('read should invoke processTickers for valid file', function () {
        var rawData = '601169\n002146\n601009'
        var parsedData = ['601169', '002146', '601009'];

        sinon.stub(fs, 'readFile').callsFake(function(fileName, callback){
            callback(null, rawData);
        });
    
        sinon.stub(stockFetch, 'parseTickers').withArgs(rawData).returns(parsedData);    

        sinon.stub(stockFetch, 'processTickers').callsFake(function(data){
            expect(data).to.be.eql(parsedData);
        });

        stockFetch.readTickerFile('dummyValidFile', function(err){throw new Error(err);});
    });


    it('read should return error if given file is empty', function(done){
        var onError = function(err){
            expect(err).to.be.eql('File dummyEmptyFile has invalid content');
            done();
        };

        sinon.stub(stockFetch, 'parseTickers').withArgs('').returns([]);
        sinon.stub(fs, 'readFile').callsFake(function(fileName, callback){
            callback(null, '');
        });

        stockFetch.readTickerFile('dummyEmptyFile', onError);
    });


    it('processTickers should call getPrice for each ticker symbol', function(){
        const stockFetchMock = sinon.mock(stockFetch);
        stockFetchMock.expects('getPrice').withArgs('601169');
        stockFetchMock.expects('getPrice').withArgs('002146');
        stockFetchMock.expects('getPrice').withArgs('601009');
        
        stockFetch.processTickers(['601169', '002146', '601009']);
        stockFetchMock.verify();
    });

    it('processTickers should call getPrice for each ticker symbol by sequence', function(){
        const stockFetchSpy = sinon.spy(stockFetch, 'getPrice');
        
        stockFetch.processTickers(['601169', '002146', '601009']);

        expect(stockFetchSpy.firstCall.calledWithExactly('601169')).to.be.true;
        expect(stockFetchSpy.secondCall.calledWithExactly('002146')).to.be.true;
        expect(stockFetchSpy.thirdCall.calledWithExactly('601009')).to.be.true;
    });
```
## Dummy
如`dummyInvalidFile`，`dummyValidFile`和`dummyEmptyFile`，该参数在程序里实际上并没有参与执行，因为`fs.readFile`方法已经被Stub了。

此即没有真正用到但又需要填充的情形。建议起个好点的名字，最好一目了然。

## Stub
Stub并不是真正的实现，主要用来在调用时快速返回预设数据。

Stub相当于把目标替换了，原本的方法不会再执行。

通常使用Stub来预设依赖数据，控制程序的行为，使得我们可以一次只测试一个我们关心的特定路径，实现代码隔离。

比如`fs.readFile`的Stub，使得程序无需真正地进行文件操作，同时可以赋予不同的返回数据，分别测试（定义）了目标方法在读文件出错，读正常文件和读空文件情形下的行为。

Stub `parseTickers`和`processTickers`，则使得该Test Case可以专注于测试`readTickerFile`，遵循单一职责原则。

在TDD（Test Driven Development）过程中，使用Stub可以帮助我们在后续程序还没实现的情况下，先验证和完成目标功能。

## Fake
Fake是用一个假的实现，来代替实际目标程序，该实现只适用于测试环境而不能用于生产环境。

上例的`onError`即是Fake的，只用来验证返回的错误信息。

另外Stub后面的`callFake`也是相同用法，虽然Stub了，但是也提供一个Fake的实现，写了些简单的代码来顺便验证它接收到的参数是不是我们所期望的。

Sinon里另外提供fake方法,结合了Spy和Stub的概念。
```javascript
var fake = sinon.fake.returns('42');
sinon.replace(console, 'log', fake);
console.log('apple pie');
// 42
```

## Mock
Mock主要是验证程序行为有没有按照我们预定的路径发生，它也可以返回预设数据，同时可以对交互进行跟踪，如调用的次数，调用的顺序。

比如`processTickers`的Test Case验证了`'processTickers should call getPrice for each ticker symbol'`。

数组参数的每个元素都会作为`getPrice`的参数调用一次。如果任何一个预期没有发生，测试会失败。

## Spy
Spy实际上是通过代理来获取目标的被调用情况，如被调用了几次，使用什么参数。

Spy可以与真实的服务进行交互，对交互进行验证或部分模拟。

上面Spy的Test Case是参照Mock的例子写出来的，同样验证了数组参数被`getPrice`调用的情形，而且是按顺序调用。

# 参考
https://sinonjs.org/   
