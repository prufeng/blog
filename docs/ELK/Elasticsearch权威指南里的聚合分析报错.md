ELK - Elasticsearch权威指南里的聚合分析报错: Text fields are not optimised for operations that require per-document field data like aggregations and sorting
====
Elasticsearch权威指南是指官网的《Elasticsearch：权威指南》。

# 聚合分析
```json
GET employee/_search
{
    "aggs": {
    "all_ages": {
      "terms": { "field": "age" }
    }
  }
}

GET employee/_search
{
    "aggs": {
    "all_interests": {
      "terms": { "field": "interests" }
    }
  }
}

```
在`interests`上进行聚合会报错，而`age`没问题。
```json
    "root_cause" : [
      {
        "type" : "illegal_argument_exception",
        "reason" : "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [interests] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ]
```

因为`interests`的`type`是`text`，而`age`不是， `text`或`annotated_text`字段`doc_values`默认为`false`。  

简单理解，就是`text`字段作为一个整体，默认没有索引。

```json
GET employee/_mapping
{
  "employee" : {
    "mappings" : {
      "properties" : {
        "about" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "age" : {
          "type" : "long"
        },
        "first_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "interests" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "last_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}
```

不过`text`分词之后的`keyword`是有索引的，因而可以对`interests.keyword`进行聚合。

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

也可以`set fielddata=true`，不过不推荐。

>Fielddata is disabled on text fields by default.       

>Fielddata can consume a lot of heap space, especially when loading high cardinality text fields. Once fielddata has been loaded into the heap, it remains there for the lifetime of the segment. Also, loading fielddata is an expensive process which can cause users to experience latency hits. This is why fielddata is disabled by default.
```json
PUT employee/_mapping 
{
  "properties": {
    "interests": {
      "type": "text",
      "fielddata": true
    }
  }
}
```

# 相关文章

[ELK - Elasticsearch权威指南里的简单搜索例子](https://github.com/prufeng/blog/blob/master/Architect/ELK%20-%20Elasticsearch%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97%E9%87%8C%E7%9A%84%E7%AE%80%E5%8D%95%E6%90%9C%E7%B4%A2%E4%BE%8B%E5%AD%90.md)
