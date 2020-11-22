### 美多商城项目

##### 1. 购物车记录合并

当用户进行登录时，需要将cookie中的购物车合并redis中。

购物车记录合并不是一个新的API接口，只是在登录流程基础上，增加一个合并的过程。

1）普通登录

2）QQ登录

怎么进行合并？(购物车数据合并的方案)

```python
假如id为2用户登录之前，
cookie中的购物车数据如下:
	{
    	11: {
        	'count': 1,
        	'selected': False
    	},
    	16: {
        	'count': 2,
        	'selected': True
    	}
	}

redis中购物车数据如下:
    cart_2: {
        '11': '2',
        '16': '1',
        '10': '1'
    }
        
    cart_selected_2: ('11', '10') 
```

合并方案：

​	合并购物车数据时，如果cookie中的购物车数据和redis购物车数据有冲突，以cookie数据为准。

​	如果没有冲突，都进行保留。

```python
cart_2: {
    '11': '1',
    '16': '2',
    '10': '1'
}
    
cart_selected_2: ('16', '10')
```



```python
{
    16: {
        'count': 2,
        'selected': True
    },
    11: {
        'count': 1,
        'selected': False
    }
}

cart_2: {
    '16': '1',
    '11': '1',
    '10': '1'
}

cart_selected_2: ()

cart_2: {
    '16': '2',
    '11': '1',
    '10': '1'
}

cart_selected_2: ('16', )
```

##### 2. 订单结算-用户结算商品信息获取

用户要结算的商品就是redis购物车中被选中的商品记录。

```http
API: GET /order/settlement/
参数:
	前端通过请求头传递jwt token数据
响应:
	{
        'freight': '运费',
        'skus': [
            {
                'id': '商品id',
                'name', '商品名称',
                'price': '商品单价',
                'default_image_url': '默认图片',
                'count': '商品数量'
            },
            ...
        ]
	}
```

##### 3. 订单保存(订单创建)

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

订单事务：mysql事务。

订单并发：多人同时下单问题。

























