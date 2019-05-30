JWT技术简单理解和实现
===
# JSON Web Token
>JSON Web Token (JWT) is an open standard ([RFC 7519](https://tools.ietf.org/html/rfc7519)) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

(https://jwt.io/introduction/)

简而言之，JWT是一个JSON信息传输的开放标准，它可以使用密钥对信息进行数字签名，以确保信息是可验证和可信任的。

# JWT结构
* Header
* Payload
* Signature

Header和Payload只是简单的base64编码，并没有加密，因而不能用来传递敏感内容。

Signature是加密的，接收方主要是靠这一部分进行验证。   
因为加密的内容较少，运用复杂一些的算法，其效率应该也是可以接受的。

![](assets/jwt-debugger.png)

# JWT用途

由JWT的结构可知，JWT并不能用来发送加密内容，而只是帮忙验证传输的内容是否中途被更改过，即所谓防篡改。

防篡改的特性使得JWT可以用来传递用户身份信息，达到服务状态保持，从而实现单点登录。

* Client请求授权
* Authorization Server返回access token
* Client使用access token去访问其他服务（资源）

![](assets/client-credentials-grant.png)

# JWT实现要点

* Client验证成功时，生成Token
* 之后的每一个请求都要携带Token
* 后台处理每一个请求都要先验证Token

# Node.js实现

* Install jsonwebtoken

https://github.com/auth0/node-jsonwebtoken

* 生成Token
```js
// sign with RSA SHA256
var jwt = require('jsonwebtoken');
var privateKey = fs.readFileSync('private.key');
var token = jwt.sign({ foo: 'bar' }, privateKey, { algorithm: 'RS256'});
```
* 验证Token
```js
// verify a token asymmetric
var cert = fs.readFileSync('public.pem');  // get public key
jwt.verify(token, cert, function(err, decoded) {
  console.log(decoded.foo) // bar
});
```
* Decode Payload
无须签名，就可以解码Header和Payload，所以千万不要误以为它们是加密的。
```js
// get the decoded payload ignoring signature, no secretOrPrivateKey needed
var decoded = jwt.decode(token);

// get the decoded payload and header
var decoded = jwt.decode(token, {complete: true});
console.log(decoded.header);
console.log(decoded.payload)
```
