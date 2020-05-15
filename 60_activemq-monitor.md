# n9e activemq监控脚本

系统需求

操作系统：Linux Python >= 2.6

主要逻辑

从activemq-server的api接口读取相关数据,n9e-collector获取数据

汇报字段
--------------------------------
| metric |  tags | type | note |
|--------|-------|------|------|
|activemq_pending|name(Queue名字)|GAUGE|队列中处于等待被消费状态消息数|
|activemq_consumers|name(Queue名字)|GAUGE|队列消费者数量|
|activemq_enqueue|name(Queue名字)|GAUGE|队列入队消息总数|
|activemq_dequeued|name(Queue名字)|GAUGE|队列完成消费的消息数|
|activemq_enqueue_rate|name(Queue名字)|COUNTER|队列入队消息的speed|
|activemq_dequeued_rate|name(Queue名字)|COUNTER|队列消费的speed|

使用方法

- 1、修改60_activemq-monitor.py脚本的url，username，password
- 2、get_ip_address函数是负责指定上报endpoint的，可以根据需要修改
- 3、将脚本放到n9e-collector的plugin目录，在采集配置中将对应的插件路径配置到到指定节点，n9e-collector会主动执行60_activemq-monitor.py脚本，60_activemq-monitor.py脚本执行结束后会输出json格式数据，由n9e-collector读取和解析数据

