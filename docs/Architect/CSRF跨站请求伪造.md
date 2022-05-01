CSRF跨站请求伪造
===

# Cross-Site Request Forgery

CSRF，Cross-Site Request Forgery，跨站请求伪造，也被称为： XSRF, One-Click attack, Sea Surf, Session Riding, Cross-Site Reference Forgery, and Hostile Linking。

CSRF是指攻击者通过某些技术手段欺骗用户，盗用其已认证的身份去执行一些恶意操作（如修改用户邮件或密码，发消息，转账和购买商品）。

CSRF漏洞与浏览器的隐式身份认证机制有关。用户在目标网页完成身份认证时，浏览器会在本地（Cookie）保存当前会话状态信息，当用户再次发送请求时，浏览器会自动携带该会话Cookie， 服务器据此判断请求来自同一用户（会话），执行请求操作。

这时假如攻击者成功诱使用户打开攻击站点，则可向目标站点发送伪造请求。由于用户已经认证过，所以浏览器将自动携带之前的会话Id，被访问网站则会认为这是用户的真实请求而去执行。

跨站是指恶意请求是由攻击站点发起，而不是用户一开始访问的可信站点。由于浏览器同源策略（Same Origin Policy）的限制，攻击者一般无法在攻击站点获取用户Cookie，而只能通过伪造请求进行攻击。

# CSRF攻击场景

典型场景如下：

* 用户登录可信站点A
* 未logout的情况下访问攻击站点B
* 攻击站点B向站点A发送恶意请求

攻击实现的难点是第二步，即如何让用户在访问A的同时刚好打开B。

常见的形式有钓鱼邮件、诈骗信息、浏览器弹出窗口（浏览器劫持）、漏洞站点代码植入等。   
比如你在操作网银时，刚好看到一封银行发送给你的（钓鱼）邮件，或者刚好浏览器弹出一个你感兴趣的新闻，然后你眼疾手快地点击了里面的链接。

攻击站点B不一定是恶意站点，可能只是有漏洞的普通网站，甚至是受欢迎的高流量网站。

B向A发送请求是通过技术手段自动实现。也就是说，当打开网页时，你就中招了，并不需要任何其他操作。所以尽管用户登录A的同时正好打开B的几率不大，但是黑客并不需要做什么，只是坐等收钱，因而这肯定也是一种受欢迎的攻击手段。

另外，大多数人都没有完成操作就立即退出登录的良好习惯。

# CSRF请求伪造

## GET

典型例子如下， `img`的情况下不需要用户点击链接，打开窗口便自动提交请求。

```html
<a href="http://bank.com/transfer.do?acct=MARIA&amount=100000">View my Pictures!</a>

<img src="http://bank.com/transfer.do?acct=MARIA&amount=100000" width="0" height="0" border="0">
```

所以一般更新操作不要用Get，因为伪造成本太低。

## POST

Post实现相对应的代码如下。

表单当然是不显示出来的，通常放在隐藏的iframe里。

```html
<form action="<nowiki>http://bank.com/transfer.do</nowiki>" method="POST">
<input type="hidden" name="acct" value="MARIA"/>
<input type="hidden" name="amount" value="100000"/>
<input type="submit" value="View my pictures"/>
</form>

<body onload="document.forms[0].submit()">
```

## XMLHttpRequest

XMLHttpRequest方法受浏览器同源策略限制，一般不会成功，除非目标站点定义了`Access-Control-Allow-Origin: *`。

但是，在JavaScript的世界里，绕过同源策略的代码却很容易找到，更不用说各种各样的浏览器漏洞了。

```html
<script>
function put() {
	var x = new XMLHttpRequest();
	x.open("PUT","http://bank.com/transfer.do",true);
	x.setRequestHeader("Content-Type", "application/json"); 
	x.send(JSON.stringify({"acct":"BOB", "amount":100})); 
}
</script>
<body onload="put()">
```

# CSRF防守策略

由以上分析可知，CSRF攻击之所以能奏效，主要是因为攻击者可以成功地伪造一个合法的请求，即目标操作的所有参数都可以被分析出来。

因此防范的策略主要是往请求中加入无法猜测的参数值，比如验证码和Token。

## 验证码

验证码是最简单有效的方法，但是因为影响用户体验，不能作为主要的解决方案。


## Anti CSRF Token

CSRF Token方法与验证码类似，只是不需要用户干预。

增加一个随机生成的Token，发送给前端，前端提交表单时包含该Token，在后台验证，验证通过才是有效请求。

一个请求提交后，Token即被消耗掉，然后重新生成新Token。所以，也要考虑同时有多个请求时的并发处理问题。

注意：

* Token要足够随机，不可预测。
* Token要注意保密，不能泄露。

比如页面如果同时有XSS（跨站脚本攻击）漏洞，则攻击者完全可以读出页面的Token值，再伪造合法的请求，这一过程一般称为XSRF，与CSRF相区别。

除了加Token，也可以考虑给参数加密，或者验证访问来源（Referrer）。

## JSON Web Token

假如我已经使用了JWT无状态App设计，还需不需要再引入CSRF Token？

答案是：不需要。

除了不是by request生成，JWT具有CSRF Token相同的特征，因而是安全的。

总的来说，避免使用Cookie进行身份认证，应该已经可以防范大多数的CSRF漏洞。

# 参考

https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)   
《白帽子讲Web安全》 —— 吴翰清
