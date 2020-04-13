重构 - Java程序太多if else怎么办
===

有人问，我的程序太多if else了，怎么办？

让发过来看看，长这样。
```java
    public void execute(boolean ba, boolean bb, boolean bc) {
        if (ba && bb && bc) {
            response = callApiByChannelName(getChannelNameForThree(aChannel, bChannel, cChannel), xLoad, userInfo);
        } else if (ba && bb && !bc) {
            response = callApiByChannelName(getChannelNameForTwo(aChannel, bChannel), xLoad, userInfo);
        } else if (ba && !bb && bc) {
            response = callApiByChannelName(getChannelNameForTwo(aChannel, cChannel), xLoad, userInfo);
        } else if (!ba && bb && bc) {
            response = callApiByChannelName(getChannelNameForTwo(bChannel, cChannel), xLoad, userInfo);
        } else if (ba && !bb && !bc) {
            response = callApiOfChannelA(aChannel, xLoad, userInfo);
        } else if (!ba && bb && !bc) {
            response = callApiOfChannelB(bChannel, xLoad, userInfo);
        } else if (!ba && !bb && bc) {
            response = callApiOfChannelC(cChannel, xLoad, userInfo);
        }
    }
```
我说你不是看过设计模式吗？
看过，可是还是不知道怎么办？

程序设计的原则简单来说就两点，首先是怎么把无关的东西分开，然后是怎么把共同的东西抽出来。

好吧，看你也听不明白，帮你分析一下。

# 先理解业务逻辑再写代码

一看你这个条件就是一个排列组合嘛，你看`getChannelNameForThree()`这个方法是从三个中选一个是吧？

然后`getChannelNameForTwo()`是从两个中选一个，剩下的不用选。

上面这四个`callApiByChannelName()`最终调用的实际上还是下面那三个方法，对吧？

而且我相信三个中选一个两个中选一个的逻辑应该是一样的，但是现在你的ifelse，却被写成了这个策略的一部分。

其实应该把它抽出来，先决定好调用哪个接口，然后再调用它，这样就根本不需要这么多ifelse了。

所以问题不在于ifelse，而是你没有真正理解业务逻辑。

代码中多几个ifelse也并不是多严重的问题，真正的问题是，如果再加一个新成员来组合，该怎么办？

另一个问题就是，这个代码再放几天，估计连你自己也搞不清楚它到底是要做什么的了。

说完他去检查业务逻辑去了，等他检查完，我的模拟重构代码也基本上写完了。

第一步优化结果如下，已经解决了ifelse多且难看的问题。
```java
    public void step1() {
        int i = getTheRightChannel();
        if (i == 1) {
            response = callApiOfChannelA(aChannel, xLoad, userInfo);
        } else if (i == 2) {
            response = callApiOfChannelB(bChannel, xLoad, userInfo);
        } else {
            response = callApiOfChannelC(cChannel, xLoad, userInfo);
        }
    }
```
他检查完之后的回复在我意料之中，不过他却兴奋得像发现新大陆。我很理解这种心情。

# 使用工厂来创建对象

下一步要考虑的是，假如要再加一个Channel，要怎么办？

按照当前的程序，需要增加一个条件，再写一个方法。如果方法比较复杂，程序必然越来越臃肿。

但观察这几个方法，只是调用的远程接口的细节有所不同，所以可以抽象成一个统一的接口。
```java
    public void step2() {
        int i = getTheRightChannel(  );
        Channel channel;
        if (i == 1) {
            channel = new ChannelA();
        } else if (i == 2) {
            channel = new ChannelB();
        } else {
            channel = new ChannelC();
        }
        response = channel.callApi(xLoad, userInfo);
    }
```
接着把`Channel`的创建放到一个统一的地方。这种方法被称为简单工厂模式。
```java
    public void step3() {
        int i = getTheRightChannel();
        ChannelSimpleFactory channelSimpleFactory = new ChannelSimpleFactory();
        Channel channel = channelSimpleFactory.createChannel(i);
        response = channel.callApi(xLoad, userInfo);
    }
```

现在若要再增加`Channel`，以上代码已经无需修改了，只需新建一个`Channel`实现类，并在工厂里增加创建该类的逻辑。

个人觉得，大多数的重构，到这一步就可以了。程序逻辑已相当清晰，扩展所需的修改也已非常简单和可预见。

进一步的重构，需要考虑成本收益比，所以最好是等到下一次需求变更的时机。

# 修改只是扩展

当然，简单工厂模式还是不符合OCP (Open-Closed Principle) 的原则。

>Open for extention, closed for modification.

程序应该设计成容易扩展的，且不需要修改的。换句话说，最好的程序是，当你修改的时候，你只是在扩展。

针对当前这个业务，要达到这种程度，可以把不同种类的`Channel`保存在配置里，再通过`List`或`Map`加载出来。

这样，每当增加新`Channel`时，只需要写新的`Channel`实现类，再把它添加到配置列表里就可以。

以下代码中`Map`的设置只是演示加载过程，实际上要放在配置里。
```java
    public void step4() {
        int i = getTheRightChannel();
        ChannelSimpleFactory channelSimpleFactory = new ChannelSimpleFactory();
        // should be in the configure
        Map map = new HashMap<Integer, Channel>();
        map.put(1, new ChannelA());
        map.put(2, new ChannelB());
        map.put(3, new ChannelC());
        channelSimpleFactory.setChannelMap(map);
        //
        Channel channel = channelSimpleFactory.createChannel(i);
        response = channel.callApi(xLoad, userInfo);
    }
```

# 策略又变了怎么办

这样修改之后，似乎很完美了，但其实还有一个地方，甚至比以上这步更值得优化。

那就是怎样选出合适`Channel`的策略，`getTheRightChannel()`，这是第二可能变更需求的地方。

想想哪天老板突然走过来说，发布之前再帮忙改改这个吧，不要随机选`Channel`了，给加个权重吧。

（此处省略一万字……）

于是又要加配置，加方法，加ifelse，老路重走。

可以考虑加一个`ChannelStrategy`接口，当更换策略时，只需要新建一个子类`ChannelWeightStrategy`注入`ChannelSimpleFactory`就可以了。

```java
    public void step5() {
        ChannelSimpleFactory channelFactory = new ChannelSimpleFactory();
        ChannelStrategy strategy = new ChannelWeightStrategy();
        channelFactory.setStrategy(strategy);
        Channel channel = channelFactory.newChannel();
        response = channel.callApi(xLoad, userInfo);
    }
```
策略模式理解起来比较简单，不再赘述，不同项目细节也可能不同，不如直接看代码。

https://github.com/prufeng/hellowork/tree/master/src/main/java/pan/rufeng/pattern/refactor/ifelsefactory

最后还有一个奇怪的问题，就是，怎么看你加了那么多的类，会不会不太好？

嗯，这个，不知道怎么说，你去看看JDK或Spring里的源码吧，看看都长什么样，或者用代码工具再扫扫自己的，对比一下。

好啦，重构适可而止，不然其他项目交不了货啦！