### 美多商城项目

##### 1. 用户中心-最近浏览

用户进入个人中心，需要显示用户最近浏览的商品信息。

1）存储用户最近浏览记录，采用什么来存？`redis`

mysql存储：用户频繁浏览商品，会频繁操作数据库。

redis存储：redis的数据存储在内存中，操作redis数据要比操作mysql要快。

2）存储用户最近浏览记录，存储什么数据？`用户浏览的商品id`

3）采用redis中哪种数据类型进行存储？

```
string: 字符串
	'history_<user_id>': <value>
		
	history_1: '1,2,3'
	history_2: 

hash: 哈希 value: 属性:值
	history: {
        history_<user_id>: <value>,
        ...
	}

list: 列表
	'history_<user_id>': [1, 2, 3]
	
set: 无序集合
	排除

zset: 有序集合
	有序集合中的每个元素都有一个权重。
```

4）历史浏览记录添加？

history_1: [5, 1, 3]

去重：将用户已经浏览商品的id先删除。

保持浏览顺序：左侧加入。

浏览记录保留：根据需求，保留最新的几个。

##### 2. 商品列表信息

```http
API: /categories/(?P<category_id>\d+)/skus/?page=<page>&page_size=<page_size>&ordering=<排序方式>
```

1）返回对应分类`category_id`商品的信息。

2）分页和排序。

##### 3. 商品搜索

根据商品名称或商品副标题进行商品的搜索。

```python
select * from tb_sku where name like '%华为%' or caption like '%华为%';
```

对于sql语句，like效率很低。

1）搜索引擎

​	索引字段: 

​		搜索引擎可以将指定数据表中的数据建立一份`索引`，索引数据中记录着索引字段和表数据之间对应的关系。

```python
{
    "1":
    {
        "django_id": "5", 
        "text": "Apple iPhone 8 Plus (A1864) 64GB 深空灰色 移动联通电信4G手机\n选【移动优惠购】新机配新卡，198优质靓号，流量不限量！"
    }，
    "2":
    {
        "django_id": "3", 
        "text": "Apple iPhone 8 Plus (A1864) 128GB 深空灰色 移动联通电信4G手机\n选【移动优惠购】新机配新卡，198优质靓号，流量不限量！"
    }
	……
}
```

搜索引擎会对索引字段的内容进行关键词拆分(`分词`)，然后记录关键词在哪些索引数据中存在。

iPhone: 1，2

2）全文检索框架

​	haystack：支持多种搜索引擎 es, slor, whoosh

​	帮助用户使用搜索引擎的功能.

​	10条数据

​	2条数据

3）建立索引数据

​	定义索引类

​	指定索引字段

​	python manage.py rebuild_index

4）定义搜索视图集

##### 购物车记录存储

1）存储购物车记录存什么数据？

使用redis存储购物车记录。

存储用户的购物车记录时，需要存储用户购物车中商品id和对应数量，还有购物车中商品的选中状态。

2）采用redis的那种数据类型？hash

```
# 保存用户购物车中添加的商品id及对应数量 hash
cart_<user_id> : {
    <sku_id>: <count>,
    ...
}

# 保存用户的购物车中商品选中状态 set: 元素是唯一的
cart_selected_<user_id>: (sku_id, )

cart_1: {
    '2': '3',
    '5': '2'
}

cart_selected_1: (2, )
```

3）用户未登录让不让添加购物车记录？

​	产品经理

4）未登录用户添加购物车记录时数据怎么存储？