Node.js RESTful API Unit Test
====
Study how to test RESTful API and how to test Express framework in Node.js.

Github: https://github.com/prufeng/autotest-node

# Install
```bash
npm i -D nyc
npm i -D mocha
npm i -D chai
npm i -D chai-http
```

# Unit Test Spec
```javascript
//app.spec.js
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
```
npm test
```
```json
  "scripts": {
    "start": "node ./bin/www",
    "test": "nyc -a mocha --recursive"
  }
```
# Reference
https://scotch.io/tutorials/test-a-node-restful-api-with-mocha-and-chai   
https://github.com/samuxyz/bookstore   
https://github.com/chaijs/chai   