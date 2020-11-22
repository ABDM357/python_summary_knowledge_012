##### 1. 支付宝支付

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

```http
API: PUT /payment/status/?支付宝参数
参数:
	通过查询字符串传递支付宝参数
响应:
	# 返回支付交易编号
	{
        'trade_id': '支付交易号'
	}
```

##### 2. 用户权限的控制

接口权限：控制用户对接口访问。

用户权限：一个用户可以对哪些数据表进行操作。

##### 3. 项目部署

1）前端静态文件服务器

​	  域名: `www.meiduo.site`

​	作用: 提供静态文件。

​	开发阶段：live-server

​	部署阶段：nginx

Django收集项目所使用的静态文件：

```python
# 设置配置项STATIC_ROOT，指定收集静态文件的保存目录
STATIC_ROOT = '收集静态文件的保存目录'

# 执行收集静态文件的命令
python manage.py collectstatic
```

配置nginx提供`front_end_pc`目录下的所有静态文件:

启动: sudo /usr/local/nginx/sbin/nginx

重启: sudo /usr/local/nginx/sbin/nginx -s reload

停止: sudo /usr/local/nginx/sbin/nginx -s stop

```bash
location / {
    # 指定网站的根目录是html
    # root html;
    root /Users/smart/Desktop/sh14_code/sh14_meiduo/front_end_pc;
    # 如果访问的是网站的根路径，默认返回根目录下的index.html
    index index.html;
}
```

2）后端API服务器

​	  域名: `api.meiduo.site`

​	作用: 提供API接口访问。

​	  开发阶段: Django提供的一个开发的web服务器。`python manage.py runserver`

​	  部署阶段: uwsgi(`遵循wsgi协议web服务器`)

uwsgi使用:

安装: pip install uwsgi

配置:

```bash
[uwsgi]
#使用nginx连接时使用，Django程序所在服务器地址
# socket=127.0.0.1:8001
# 直接做web服务器使用，Django程序所在服务器地址
http=127.0.0.1:8001
# 项目目录
chdir=/Users/smart/Desktop/sh14_code/sh14_meiduo/meiduo_mall
# 项目中wsgi.py文件的目录，相对于项目目录
wsgi-file=meiduo_mall/wsgi.py
# 进程数
processes=4
# 线程数
threads=2
# uwsgi服务器的角色
master=True
# 存放进程编号的文件
pidfile=uwsgi.pid
# 日志文件，因为uwsgi可以脱离终端在后台运行，日志看不见。我们以前的runserver是依赖终端的
daemonize=uwsgi.log
# 指定依赖的虚拟环境
virtualenv=/Users/smart/.virtualenvs/django
```

启动: uwsgi --ini '配置文件路径'

停止: uwsgi --stop 'pid文件路径'





























