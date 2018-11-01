TypeScript Unit Test with Mocha and Istanbul
====

# Nyc and Mocha
Supposed Nyc and Mocha have been installed. If not, can refer to this link below.

https://blog.csdn.net/prufeng/article/details/83043246

```
npm install -D source-map-support
```

## package.json - nyc
```json
  "nyc": {
    "extension": [
      ".ts",
      ".tsx"
    ],
    "exclude": [
      "**/*.d.ts"
    ],
    "reporter": [
      "clover",
      "lcovonly"
    ],
    "all": true  
  },
```

## test/mocha.opts
```
--require ts-node/register
--require source-map-support/register
--recursive
--reporter mocha-bamboo-reporter
```
Works without ts-node from my test, not see any difference in the report.

# SonarQube
## Install SonarQube Plugin - SonarTS

## sonar.properties
```
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.typescript.lcov.reportPaths=coverage/lcov.info
```
Works without sonar.typescript.lcov.reportPaths configure from my test. 

# Reference
https://istanbul.js.org/docs/tutorials/typescript/

