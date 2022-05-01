Elasticsearch什么时候使用Data Transform和Rollup Jobs
====
# 问题场景
两个log，一个是信息发送记录，一个是信息接收记录，都load到同一个index里，想要通过查询这个index来监控信息是否发送成功，亦即判断发送log里出现的信息id，能不能在接收log里找到，找到就算成功，否则发送告警邮件。
我想到的方法是，用painless script，分别按log类型不同aggregate之后，再循环判断发送的id是不是都能在接收日志里找到，不过painless script功能比较简单，测试比较麻烦。

Elastic Architect推荐用Data Transforms。

# Data Transforms
试用一下，发现所谓Data Transforms，其实是定时将一个index的数据转换到另一个新的index。当我们想在统计数据的基础上再做展示时，就非常有用了，特别是它不但包括了常规的Aggretion，还可以Group by。暂时还不太清楚Group by的背后是怎么实现的。

不过数据转换有一个转换时点的问题，就是在某一时刻，部分数据已经转换到新index，可是如果源index还在持续更新，新的数据只能等到下次转换再统计，这样就导致实际想要的数据被截断了，得到的不是我们想要的结果。虽然理论上来说数据不可避免会在某一时刻被截断，但直接在源数据上查询，新的查询就会包含最新的数据，得出正确的结果，但转换不一样，下次再转换，并不会修正之前已经转换的记录。这样看起来，在固定的时间用来做统计和备份是有价值的，但用做实时告警似乎就不太严谨了，可能会误报偏多。

Elastic对Data Transforms的目标表述如下：
>Use transforms to pivot existing Elasticsearch indices into summarized or entity-centric indices.

## Transform API
```
GET _transform/<job_id>
GET _transform/<job_id>/_stats
POST _transform/<job_id>/_start
POST _transform/<job_id>/_stop
post _transform/<job_id>/_update
```

# Data Rollup Jobs

相比之下，Rollups功能则明确表示，它是用来备份数据的，使我们在源数据删除以后，仍能获得历史数据的概况。

有些数据长期保留的价值偏低，这时，保留一个类似统计快照的信息或许就已经足够了。

>Summarize and store historical data in a smaller index for future analysis.

## /job/
```
PUT /_rollup/job/<job_id>: Create a rollup job
GET /_rollup/job: List rollup jobs
GET /_rollup/job/<job_id>: Get rollup job details
POST /_rollup/job/<job_id>/_start: Start a rollup job
POST /_rollup/job/<job_id>/_stop: Stop a rollup job
DELETE /_rollup/job/<job_id>: Delete a rollup job
```
## /data/
```
GET /_rollup/data/<index_pattern>/_rollup_caps: Get Rollup Capabilities
GET /<index_name>/_rollup/data/: Get Rollup Index Capabilities
```
## /<index_name>/
```
GET /<index_name>/_rollup_search: Search rollup data
```
