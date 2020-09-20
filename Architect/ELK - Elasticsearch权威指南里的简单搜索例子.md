ELK - Elasticsearch权威指南里的简单搜索例子
====
Elasticsearch权威指南是指官网的[《Elasticsearch：权威指南》](https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html)。

例子跟官网不一样，是因为类型（Type）这种用法现在已经被抛弃了，所以缺省类型都是`_doc`。

# 建立索引

```json
PUT /employee/_doc/1
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
PUT /employee/_doc/2
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}

PUT /employee/_doc/3
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
```

# 检索文档
```
GET employee/_doc/1

#index info
GET employee
```

# 轻量搜索
```
GET employee/_search
GET employee/_search?q=last_name:Smith
```

# 查询表达式
```json
GET employee/_search
{
  "query": {
    "match": {"last_name": "Smith"}
  }
}

GET employee/_search
{
    "query": {
        "bool":{
            "must": {
                "match": {"last_name": "Smith"}
            },
            "filter": {
                "range": {
                  "age": {
                    "gt": 30
                  }
                }
            }
        }
    }
}

```

# 全文搜索
```
GET employee/_search
{
    "query": {
        "match": {
          "about": "rock climbing"
        }
    }
}

```

# 短语搜索
```
GET employee/_search
{
    "query": {
        "match_phrase": {
          "about": "rock climbing"
        }
    }
}
```

# 高亮搜索
```
GET employee/_search
{
    "query": {
        "match_phrase": {
          "about": "rock climbing"
        }
    },
    "highlight": {
      "fields": {
        "about": {}
      }
    }
}
```

# 聚合分析

## 员工兴趣统计
```json
GET employee/_search
{
    "aggs": {
    "all_interests": {
      "terms": { "field": "interests" }
    }
  }
}

```
在`interests`上进行聚合会报错。
```json
    "root_cause" : [
      {
        "type" : "illegal_argument_exception",
        "reason" : "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [interests] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ]
```
正确写法应该是：

```json
GET employee/_search
{
    "aggs": {
    "all_interests": {
      "terms": { "field": "interests.keyword" }
    }
  }
}
```

具体分析看这里：[ELK - Elasticsearch权威指南里的聚合分析报错: Text fields are not optimised for operations that require per-document field data like aggregations and sorting](https://github.com/prufeng/blog/blob/master/Architect/ELK%20-%20Elasticsearch%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97%E9%87%8C%E7%9A%84%E8%81%9A%E5%90%88%E5%88%86%E6%9E%90%E6%8A%A5%E9%94%99.md)

## 某些员工兴趣

可以加组合查询条件：
```json
GET employee/_search
{
  "query": {
    "match": {
      "last_name": "smith"
    }
  },
  "aggs": {
    "all_interests": {
      "terms": {
        "field": "interests.keyword"
      }
    }
  }
}
```

## 兴趣的平均年龄

也可以汇总分析，有某个兴趣爱好的所有员工的平均年龄。

```json
GET employee/_search
{
    "aggs" : {
        "all_interests" : {
            "terms" : { "field" : "interests.keyword" },
            "aggs" : {
                "avg_age" : {
                    "avg" : { "field" : "age" }
                }
            }
        }
    }
}
```
# 相关文章

[ELK - Elasticsearch权威指南里的聚合分析报错: Text fields are not optimised for operations that require per-document field data like aggregations and sorting](https://github.com/prufeng/blog/blob/master/Architect/ELK%20-%20Elasticsearch%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97%E9%87%8C%E7%9A%84%E8%81%9A%E5%90%88%E5%88%86%E6%9E%90%E6%8A%A5%E9%94%99.md)
