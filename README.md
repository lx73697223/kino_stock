# 股票小作手

- configs                  配置类. 可通过 local_config.LocalConfig.init_config_file_path 属性定位的配置文件定义
- core_utils              跟业务无关的普通工具函数
- feed_data               获取第三方数据
- messaging               消息/通知发送工具
- repository              数据存储工具
- schedule                定时任务
- strategy                策略/算法
- tools                   脚本

--- 

## 需要安装的库或软件

- Python
    > 3.8
- 依赖包以及python环境管理工具
    > Anaconda：4.0
    > http://www.continuum.io/downloads
- 股票数据接口包
    > 1.2.26
    > pip install tushare
- 定时任务
    > 3.6.3
    > pip install apscheduler
- 数据库操作ORM框架
    > 1.3.18
    > pip install sqlalchemy
- mysql数据库连接驱动
    > 2.2.9
    > pip install mysql-connector
--- 

## 2020-07-06
```
扫描沪深股市所有的股票, 设置一个门槛, 如过滤交易额在5亿以下的，
监控资金量/交易量突然上涨的，目的是在中低位发现可能大涨的股票。
```
