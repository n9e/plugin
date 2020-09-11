# n9e nsq监控脚本

系统需求

操作系统：Linux Python >= 2.6

主要逻辑

从nsq-server的api接口读取相关数据,n9e-collector获取数据

汇报字段
--------------------------------
| metric |  tags | type | note |
|--------|-------|------|------|
|nsq.$topic_name|  |GAUGE|队列中处于等待被消费状态消息数|


使用方法

- 1、修改60_nsq.py脚本的url接口地址，一般采集本机修改端口
- 2、get_ip_address函数是负责指定上报endpoint的，可以根据需要修改
- 3、将脚本放到n9e-collector的plugin目录，在采集配置中将对应的插件路径配置到到指定节点，n9e-collector会主动执行60_nsq.py脚本，60_nsq.py脚本执行结束后会输出json格式数据，由n9e-collector读取和解析数据

