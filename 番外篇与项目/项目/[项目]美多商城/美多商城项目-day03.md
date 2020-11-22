##### 登录状态保持

1）session

```python
1. 接收用户名和密码
2. 校验用户名和密码是否正确
3. 保存用户的登录状态(session)
	session['user_id'] = 2
    session['username'] = 'smart'
    session['mobile'] = '13155667788'
4. 返回应答，登录成功
```

session认证存在的两个问题:

1）session信息存在服务器端，如果登录用户过多，会占用服务器过多空间。

2）session是依赖于cookie中，每个客户端对应的session标识存储一个cookie中，通过标识就可以找到客户端对应session信息，可能会出现安全问题CSRF(跨站请求伪造)

2）jwt (Json Web token) (替代session认证机制)

```python
1. 接收用户名和密码
2. 校验用户名和密码是否正确
3. 保存用户的登录状态(jwt token)
	服务器生成(签发)一个jwt token，在token中保存登录用户的身份信息
    类似于: (公安局)服务器 -> jwt token(用户身份证)
4. 返回应答，将jwt token返回给客户端
```

在之后需要进行用户认证时，客户端需要将jwt token发送给服务器，由服务器对jwt token有效性进行验证。

##### JWT token数据格式

jwt token就是一段字符串，字符串分为3部分，每一部分用.隔开。

1）header(头部)

```
{
    "token类型声明",
    "加密算法声明"
}
```

base64加密(加密之后的内容就是头部) -> 很容易被解密

base64编码->base64解码

2）payload(载荷) (保存有效信息)

```
{
    "id": 2,
    "username": "smart",
    "mobile": "13155667788",
    "email": ...
    "exp": "token有效时间"
}
```

base64编码

3）signature(签名) -> 防止jwt token被伪造

将header和payload字符串进行拼接，用.隔开，然后使用一个密钥(secret key)进行加密，加密之后的内容就是签名。

jwt token是由服务器生成，密钥保存在服务器端。

假如服务器密钥: abc



我是一个伪造jwt token的人:

```
{
    "token类型声明",
    "加密算法声明"
}

{
    "id": 3,
    "username": "smart2",
    "mobile": "13155669999",
    "email": ...
    "exp": "token有效时间"
}

伪造密钥: 123
```

##### 用户登录

API: POST /authorizations/

参数: 

{

​	"username": "用户名"，

​	"password": "密码"

}

响应: 

{

​	"user_id": "用户id",

​	"username": "用户名",

​	"token": "jwt token"

}

##### 支持手机号和用户名登录

obtain_jwt_token

 -> 进行用户名和密码验证时调用Django认证系统中的authenticate

from django.contrib.auth import authenticate

-> 调用Django认证后端类中authenticate

from django.contrib.auth.backends import ModelBackend

```python
 def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据用户名和密码进行校验，如果用户名和密码正确，返回user，否则返回None
        # 此方法仅执行用户名和密码校验，不支持手机号
        pass
```

##### QQ登录

1）成为QQ开发者

2）创建开发者应用