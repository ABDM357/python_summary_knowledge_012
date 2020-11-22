### 美多商城项目

##### 1. 订单保存(订单创建)

```http
API: POST /orders/
参数:
	前端通过请求头传递jwt token数据
	{
        'address': '收货地址id',
        'pay_method': '支付方式'
	}
响应:
	{
        'order_id': '订单id'
	}
```

订单保存基本流程：

​	1）向订单基本信息表添加一条记录

​	2）订单中包含几个商品，就需要向订单商品表中添加几条记录

​	3）清除购物车中对应的记录

##### 2. 订单事务

对于订单保存的过程，其中的数据库操作，要么都应该成功，要么都应该失败。

mysql事务：一组mysql语句，放在同一事务中，要么都成功，要么都失败。

1）mysql事务基本操作:

​	begin或start transaction：手动开启一个mysql事务。

​	commit: 事务提交，让事务中sql语句的执行结果永久有效。

​	rollback: 事务回滚，撤销事务中sql语句的执行结果。

2）mysql事务的保存点:

​	在mysql事务中，可以设置事务保存点，在进行事务语句回滚时可以只回滚到某个保存点。

​	  savepoint `保存点名称`： 设置mysql事务保存点。

​	  rollback to `保存点名称`: 回滚事务语句到保存点的位置，保存点之后sql语句的执行结果会被撤销。

3）django使用事务:

```python
from django.db import transaction

with transaction.atomic():
    # 在with语句块中代码，凡是涉及到数据库操作的代码，都会放到同一个事务中
    
    # 设置一个事务保存点
    sid = transaction.savepoint()
    
    # ...
    
    # 回滚到指定的事务保存点
    trnasaction.savepoint_rollback(sid)
```

##### 3. 订单并发

多个人同时购买同一件商品，可能会产生订单并发问题。

订单并发问题解决：

1）悲观锁：

​		在事务中查询数据的时候尝试对数据进行加锁(互斥锁), 获取到锁的事务可以对数据进行操作，获取不到			锁的事务会阻塞，直到锁被释放。

2）乐观'锁'：

​	本质不是锁，乐观锁本质上不是加锁，查询数据的时候不加锁，对数据进行修改的时候需要进行判断,修改失败需要重新进行尝试。

3）celery任务队列。

​	把订单保存代码放到celery的任务中，只启动一个worker。

mysql事务的隔离级别:

| 隔离级别                        | 说明                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| **Repeatable read**（可重复读） | 在一个事务中执行一个查询语句，获取到结果永远和第一次获取的结果相同，即使其他事务把数据进行修改而且已经提交，当前事务仍然获取不到更新之后结果。 |
| **Read committed**（读取已提交) | 其他事务进行数据的修改并且提交之后，当前事务能获取到更新之后的结果。 |

>  **Repeatable read**是mysql事务默认隔离级别。

修改mysql事务的隔离级别:

1）编辑mysql配置文件

​	sudo vi /etc/mysql/mysql.conf.d/mysqld.conf

2）修改配置信息

```shell
[mysqld]
 28 #
 29 # * Basic Settings
 30 #
 31 user        = mysql
 32 pid-file    = /var/run/mysqld/mysqld.pid
 33 socket      = /var/run/mysqld/mysqld.sock
 34 port        = 3306
 35 basedir     = /usr
 36 datadir     = /var/lib/mysql
 37 tmpdir      = /tmp
 38 lc-messages-dir = /usr/share/mysql
 39 skip-external-locking
 40 # 将mysql事务的隔离级别设置为读取已提交
 41 transaction-isolation=READ-COMMITTED
```

3）重启mysql服务

​	sudo service mysql restart

##### 4. 接入支付宝

线上环境:

​	1）登录支付宝开发平台

​	2）创建开发应用，设置应用信息并等待审核

​	3）审核通过之后应用上线，然后完成签约。

沙箱环境: 是对支付宝真实环境的模拟，可以让开发者不创建线上应用就可以进行开发。

python版本支付宝SDK: `pip install python-alipay-sdk --upgrade`

##### 5. 支付宝支付

1）返回支付宝支付网址和参数API

```http
API: GET /orders/(?P<order_id>\d+)/payment/
参数:
	请求头传递jwt token数据
	在url地址中传递订单id
响应:
	# 返回支付网址和参数
	{
        'alipay_url': '支付网址'
	}
```

2）保存支付结果API











