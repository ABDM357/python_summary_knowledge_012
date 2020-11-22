### DRF框架

##### 1. 授课思路说明

​	web网站2种开发模式(前后端不分离&前后端分离)

​	-> Restful API设计

​	-> Django基础知识自定义Rest API接口

​	-> rest api所做工作

​	-> DRF框架学习。

##### 2. web开发模式

​	新经资讯->首页->加载新闻信息

​	前后端不分离: 前端看到的效果最终是由后端进行控制的。

​	前后端分离: 后端只返回前端所需要的数据，至于怎么进行展示是由前端自己控制。

##### 3. RestAPI接口风格

​	前后端分离开发中广泛采用的一种API设计风格。

​	关键点：

​	1）url地址中尽量使用名词，不要出现动词。

​	2）执行不同的操作时，选择不同的请求方式。

​		GET 获取

​		POST 新增

​		PUT 修改

​		DELETE 删除

​	3）过滤参数放在查询字符串中。

​	4）响应状态码的选择。

​		200：获取或修改

​		201：新建

​		204：删除

​		400：客户端请求有误

​		404：客户端请求的资源找不到

​		500：服务器出错

​	5）响应数据返回json。		

```python
GET /books/ -> 返回所有图书信息
POST /books/ -> 返回新建的图书信息
GET /books/id/ -> 返回指定图书信息
PUT /books/id/ -> 返回修改的图书信息
DELETE /books/id/ -> 返回空文档
```

##### 4. 序列化和反序列化

​	序列化: 将模型类对象转成python字典或json数据，这个过程可以叫做序列化。

​	反序列化: 将python字典或json数据转成模型类对象，这个过程可以叫做反序列化。

##### 5. DRF框架中序列化器Serializer

​	序列化类的功能：进行序列化和反序列化。

​	序列化: 将对象转化为字典数据。

​	反序列化: 

​		1）数据校验。

​		2）数据保存(新增&更新)

​	定义序列化器类:

​		继承Serializer或ModelSerializer

```python
from rest_framework import serializers

# serializers.Serializer: 定义任何序列化器类都可以直接继承自这个类。
# serializers.ModelSerializer: 如果定义的序列化器类对应某个模型类，则可以直接继承自这个类

class User(object):
	"""用户类"""
	def __init__(self, username, age):
		self.username = username
		self.age = age

class UserSerializer(serializers.Serializer):
	"""序列化器类"""
	# 定义序列化器类字段
	# 字段名 = serializers.字段类型(选项参数)
	username = serializers.CharField()
	age = serializers.IntegerField()
	
user = User('smart', 18)
{
    "username": "smart",
    "age": 18
}

serializer = UserSerializer(user)
serializer.data

"hello"
```



