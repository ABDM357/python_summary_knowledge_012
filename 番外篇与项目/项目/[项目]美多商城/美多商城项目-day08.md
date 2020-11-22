##### 1. 用户中心-最近浏览

1. 什么时需要存储用户的浏览记录？

   答: 当用户浏览商品详情页面的时候，需要记录用户的浏览记录。

2. 把历史浏览记录存储在哪里？

   答:

   mysql存储: 用户频繁的浏览商品，需要频繁去操作数据，效率有所下降。

   redis存储: 从redis中存取数据，效率要比mysql数据库要快得多。

3. 存储什么数据？

   答: 存储用户浏览的商品的sku_id。

4. 采用redis中哪种数据类型进行存储？list

   答:

   ```
   string: 字符串
   	history_<user_id>: '1,2,3'
   
   hash: 哈希   key: <field>: <value>
   	history: {
           history_<user_id>: '1,2,3',
           ...
   	}
   
   list: 列表:  key: [<value>, <value>, ...]
   	histroy_<user_id>: [6, 5, 1, 2, 3]
   
   set: 无序集合 	key: (<value>, ...)
   	pass
   	
   zset: 有序集合	
   ```

5. 添加浏览记录过程？

   答: 

   history_2: [1, 2, 3]

   去重：如果用户已经浏览过该商品，先将商品id从列表中移除。lrem

   左侧加入: 保持浏览顺序。lpush

   截取: 只保留最近几条浏览记录。ltrim

##### 2. 历史浏览添加API

```http
API: POST /browse_histories/
参数:
	商品sku_id
	前端在请求头传递jwt token
响应: 
	{
    	'sku_id': <sku_id>
	}
```

##### 3. 历史浏览获取API

```http
API: GET /browse_histories/
参数:
	前端在请求头传递jwt token
响应:
	[
        {
            'id': '商品id',
            'name': '名称',
            'price': '价格',
            'defautl_image_url': '默认图片',
            'comments': '评论量'
        },
        ...
	]
```

##### 4. 商品列表信息获取API

根据第三级分类id获取商品的信息，分页并支持3种排序方式。

```http
API: GET /categories/(?P<category_id>\d+)/skus/?page=<页码>&page_size=<页容量>&ordering=<排序字段>
参数: 
	...
响应: 
	...
```

1）返回所有对应第三级分类下所有商品的信息。

2）分页和排序。

##### 5. 商品搜索

需求: 根据商品的名称或者商品副标题搜索商品的信息。

'iPhone'

```http
select * from tb_sku where name like '%iPhone%' or caption like '%iPhone%';
```

对于数据库搜索语句，like效率很低。

1）搜索引擎

​	搜索引擎可以将数据表的中建立一份索引数据(`维护了索引字段和表数据之间对应关系`)，搜索引擎会对`索引字段`的内容进行关键词拆分，拆分之后记录关键词在哪些索引数据中存在。

例如：es slor whoosh

2）全文检索框架: haystack

​	a）帮助用户使用搜索来使用搜索引擎功能。

​	b）帮助用户根据索引数据查询出表中的数据信息。

3）haystack对接es实现商品搜索

​	a）在es中建立索引数据。

​		定义索引类

​		指定索引字段中包含内容

​		python manage.py rebuild_index

​	b）定义搜索视图

##### 6. 购物车记录存储

需求: 用户是否登录，都可以进行购物车记录添加。

1）登录用户的购物车记录存储

​	a）购物车记录存储到redis。

​	b）添加购物车记录时，需要保存哪些数据？

​		答：`添加商品sku_id`: `对应数量count`

​		购物车中记录选中状态。

​	c）采用redis中哪种数据格式？

```http
	# hash: 记录用户购物车中添加的商品id和商品数量
	cart_<user_id>: {
        <sku_id>: <value>,
        <sku_id>: <value>,
        ...
	}
	
	# set: 存储用户购物车商品的勾选状态(存储被勾选的商品id)
	cart_selected_<user_id>: (<sku_id>, <sku_id>, ...)
	
	
	# 例如:
		id为2的用户购物车记录如下:
			id为3的商品添加5件，已经勾选
			id为1的商品添加2件，未勾选
			id为5的商品添加3件，已经勾选
		
        # hash
		cart_2: {
            '3': '5',
            '1': '2',
            '5': '3'
		}
	
		# set
		cart_selected_2: ('3', '5')
```

2）未登录用户的购物车记录存储

​