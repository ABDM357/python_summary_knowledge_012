### 美多商城项目

##### 用户中心-个人信息

```python
API: GET /user/
参数: 客户端需要将Jwt token数据传递给服务器(通过请求头)
响应: 
	{
        'id': '用户id',
        'username': '用户名',
        'mobile': '手机号',
        'email': '邮箱',
        'email_active': '邮箱是否激活'
	}
```

##### 用户中心-邮箱设置

```python
API: PUT /email/
参数: 
	客户端需要将Jwt token数据传递给服务器(通过请求头)
	email
响应:
	{
        'id': '用户id',
        'email': '用户邮箱'
	}
```

##### 用户中心-邮箱激活

```python
API: PUT /emails/verification/?token=<token>
参数: token
响应: 
	{
        'message': 'OK'
	}
```

##### 用户中心-收货地址

1）登录用户收货地址列表显示

2）收货地址添加、编辑、删除

3）设置默认收货地址

4）设置收货地址的标题

5）省市县地区的获取。

##### 省市县地区

一个省下面有很多市，一个市下面有很多县。自关联

| id     | name   | parent_id |
| ------ | ------ | --------- |
| 200001 | 江苏省 | NULL      |
| 200010 | 南京市 | 200001    |
|        |        | `         |

```
area = Area.objects.get(id='200001') # 由省查市，由1查多，一对象.多类名_set.all()
# 查询江苏省下级市的信息
area.area_set.all()

area = Area.objects.get(id='200010') # 由市查省，由多查1，多对象.外键关联属性
# 查询南京市的上级省信息
area.parent
# 查询南京市的下级地区信息
area.area_set.all()

area.subs.all()
```

1）获取所有省级地区的信息。

```python
API: GET /areas/
参数: 无
响应:
    返回所有省级地区的信息。
    [
        {
            'id': '地区id',
            'name': '地区名称'
        },
        {
            'id': '地区id',
            'name': '地区名称'
        },
        ...
    ]
```

2）选中某个省的时候，获取省下面的市的信息。

```python
API: GET /areas/省id/
参数: 省id
响应: 
	{
        'id': '省id',
        'name': '省名称',
        'subs': [
            {
                'id': '市id',
                'name': '市名称'
            },
            ...
        ]
	}
```

3）选中某个市的时候，获取市下面的县的信息。

```python
API: GET /areas/市id/
参数: 市id
响应: 
	{
        'id': '市id',
        'name': '市名称',
        'subs': [
            {
                'id': '县id',
                'name': '县名称'
            },
            ...
        ]
	}
```



```
{
    id: '县id',
    name: '县名称',
    subs: [
        
    ]
}
```











