发现git bash里curl命令也可以用，挺方便的，可以用来简单测试RESTful API。

## 1. GET
curl localhost:3000

curl -X GET localhost:3000

include header:
curl -i localhost:3000

verbose info:
curl -v localhost:3000

curl -v -X GET localhost:3000/users
curl -v -X GET localhost:3000/users/1

## 2. POST
curl -v -d "id=1&name=user1&age=18" localhost:3000/users

Note: Unnecessary use of -X or --request, POST is already inferred.
curl -v -X POST -d "id=1&name=user1&age=18" localhost:3000/users

curl -v -H "Content-type: application/json" -X POST -d '{"id":"1","name":"user1", "age": "19"}' localhost:3000/users

curl -H "Content-type: application/json" -X POST -d '{"id":"1","name":"user1", "age": "19"}' localhost:3000/users

## 3. PUT
curl -v -X PUT -d "id=1&name=user1&age=127" localhost:3000/users/1

curl -v -H "Content-type: application/json" -X PUT -d '{"name":"user1", "age": "18"}' localhost:3000/users/1

## 4. DELETE
curl -v -X DELETE localhost:3000/users/1
