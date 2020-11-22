### 美多商城项目

##### 1. 购物车数据存储

需求:

​	用户不管是否登录，都可以进行购物车记录添加。

1）登录用户购物车记录存储。

​	a）在redis中保存用户的购物车记录。

​	b）保存购物车记录时存什么数据？

​		答: ` 商品id`:`数量`。    `购物车记录勾选状态`

​	c）采用redis中哪种数据格式？

​	答:

```python
	# hash: 保存用户购物车记录中添加的商品id和对应数量
	cart_<user_id>: {
        <sku_id>: <value>,
        <sku_id>: <value>,
        ...
	}
     
   	# set: 保存用户购物车记录勾选状态(保存勾选商品id)
    # 集合中元素唯一
    cart_selected_<user_id>: (<sku_id>, <sku_id>, ...)
        
    # 例如:
    cart_2: {
        '1': '3',
        '5': '2',
        '3': '1'
    }
        
    id为2的用户购物车记录:
        id为1的商品加了3件，
        id为5的商品加了2件，
        id为3的商品加了1件，
        
   	cart_selected_2: ('1', '3')
    id为2的用户的购物车记录勾选状态:
        id为1商品和id为3的商品被勾选。
```

2）未登录用户的购物车记录存储。

存储在客户端浏览器。cookie

```
{
    '<sku_id>': {
        'count': '<count>',
        'selected': '<selected>',
    },
    '<sku_id>': {
        'count': '<count>',
        'selected': '<selected>',
    }
    ...
}
```

`json`：

​	json.dumps(dict): 将python字典转换成json字符串。

​	json.loads(json_str): 将json字符串转换成python字典。

`pickle`:

​	pickle.dumps(obj): 将obj转换成bytes字节流

​	pickle.loads(bytes字节流)：将bytes字节流转换成obj

`base64`:

​	base64.b64encode(byte字节流): 将byte字节流进行base64编码，返回编码之后内容(bytes字节流)

​	base64.b64decode(bytes字节流&str): 将参数内容进行base64解码，返回解码之后内容(bytes字节流)

`设置购物车cookie数据`:

​	res = base64.b64encode(pickle.dumps(cart_dict)).decode()

`解析cookie购物车数据`:

​	res = pickle.loads(base64.b64decode(cart_data))

##### 2. 购物车记录添加

```http
API: POST /cart/
参数:
	前端通过请求头传递jwt token数据
	{
        'sku_id': <sku_id>,
        'count': <count>,
        'selected': <selected>, # 可以不传，默认勾选
	}
响应:
	{
        'sku_id': <sku_id>,
        'count': <count>,
        'selected': <selected>
	}
```

##### 3. 购物车记录获取

```http
API: GET /cart/
参数:
	前端通过请求头传递jwt token数据
响应:
	[
        {
            'id': '商品id',
            'name': '商品名称',
            'price': '价格',
            'default_image_url': '默认图片',
            'count': '数量',
            'selected': '勾选状态',
        },
        ...
	]
```

##### 4. 购物车记录修改

```http
API: PUT /cart/
参数:
	前端通过请求头传递jwt token数据
	{
        'sku_id': '商品id',
        'count': '修改数量结果',
        'selected': '勾选状态'
	}
响应:
	{
        'sku_id': '商品id',
        'count': '修改数量结果',
        'selected': '勾选状态'
	}
```

##### 5. 购物车记录删除

```http
API: DELETE /cart/
参数:
	前端通过请求头传递jwt token数据
	{
        'sku_id': '商品id'
	}
响应:
	status=204
```

##### 6. 购物车记录全选和全不选

```http
API: PUT /cart/selection/
参数:
	前端通过请求头传递jwt token数据
	{
        'selected': <selected>, # 如果为True, 全部都选中，为False, 全部不选中
	}
响应:
	{
        'message': 'OK'
	}
```

##### 7. redis操作命令

`hash命令`：

1）hincrby(key, field, value)

​	给hash中field属性值累加一个value，如果field不存在，新建一个属性和值

2）hgetall(key)

​	返回hash中所有属性和值

3）hset(key, field, value)

​	将hash中指定属性field的值设置为value

4）hdel(key, *fields)

​	删除hash中对应的属性和值，有则删除，无则忽略

5）hkeys(key)

​	返回hash中所有属性

`set命令`:

1）sadd(key, *members)

​	向set中添加元素，不需要关注是否重复，set中元素唯一

2）smembers(key)

​	获取set中所有元素

3）srem(key, *members)

​	从set中移除元素，如果元素不存在，直接忽略



