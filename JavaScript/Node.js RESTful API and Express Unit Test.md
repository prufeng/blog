Node.js RESTful API和Express单元测试
====
本文主要研究Node.js RESTful API和Express框架的单元测试。

关于Mocha和Istanbul的详细使用，请参考：[使用Mocha和Istanbul实现Node.js单元测试和覆盖率](https://blog.csdn.net/prufeng/article/details/83043246)

Github: https://github.com/prufeng/autotest-node

# Install
```bash
npm i -D nyc
npm i -D mocha
npm i -D chai
npm i -D chai-http
```

# Unit Test Spec
创建单元测试文件app.spec.js。   
chai主要用来测试HTTP request，done用来保证异步测试完成之后mocha才返回结果。  
```javascript
let chai = require('chai');
let chaiHttp = require('chai-http');
let app = require('../app');

let should = chai.should();
chai.use(chaiHttp);

describe('App', () => {
    it('should respond status 200', (done) => {
      chai.request(app)
          .get('/')
          .end((err, res) => {
                res.should.have.status(200);
            done();
          });
    });
    it('should GET the users response', (done) => {
        chai.request(app)
            .get('/users')
            .end((err, res) => {
                  res.should.have.status(200);
                  res.text.should.equal('respond with a resource');
              done();
            });
      });

      it('should respond status 404', (done) => {
        chai.request(app)
            .get('/wrongUrl')
            .end((err, res) => {
                  res.should.have.status(404);
              done();
            });
      });
});
```
# Run Test
## package.json
`-a`用来覆盖所有代码文件，`--recursive`表示包含子目录。

```json
  "scripts": {
    "start": "node ./bin/www",
    "test": "nyc -a mocha --recursive"
  }
```
## npm test
```
npm test
```

```bash
  App
GET / 200 527.550 ms - 170
    v should respond status 200 (550ms)
GET /users 200 1.022 ms - 23
    v should GET the users response
GET /wrongUrl 404 11.877 ms - 2583
    v should respond status 404

  Calculator
    add
      v add(1,2) should return 3
    minus
      v minus(1,2) should return -1

  Array
    #indexOf()
      v should return -1 when the value is not present


  6 passing (588ms)

-----------------|----------|----------|----------|----------|-------------------|
File             |  % Stmts | % Branch |  % Funcs |  % Lines | Uncovered Line #s |
-----------------|----------|----------|----------|----------|-------------------|
All files        |      100 |       50 |      100 |      100 |                   |
 autotest        |      100 |       50 |      100 |      100 |                   |
  app.js         |      100 |       50 |      100 |      100 |             34,37 |
  calc.js        |      100 |      100 |      100 |      100 |                   |
 autotest/routes |      100 |      100 |      100 |      100 |                   |
  index.js       |      100 |      100 |      100 |      100 |                   |
  users.js       |      100 |      100 |      100 |      100 |                   |
-----------------|----------|----------|----------|----------|-------------------|
```
# Reference
https://scotch.io/tutorials/test-a-node-restful-api-with-mocha-and-chai   
https://github.com/samuxyz/bookstore   
https://github.com/chaijs/chai   
