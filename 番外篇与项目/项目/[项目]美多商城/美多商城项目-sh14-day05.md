### 美多商城项目

##### 1. 地址管理-缓存

/areas/

/areas/200001/

省市县地区信息的缓存: 

​	将地区API接口的返回结果直接放到缓存中，再次使用的时候直接从缓存中获取结果，从而提高网站性能。

##### 2. 地址管理-默认地址

在用户User模型类中添加一个`default_address`用于记录用户的默认地址。

```python
class User(AbstractUser):
	"""用户模型类"""
	# ...
	default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')
```

##### 3. 商品部分-数据表

1）SPU和SKU概念

SPU: 一组特性相同的商品的统称。例如: `IPhoneX`

SKU: 具体某一个特定规格的商品。例如:` IPhoneX 红色 256G 全网通`

2）商品表举例

`商品SPU表`:

| id   | name    |
| ---- | ------- |
| 1    | IPhoneX |

`商品SKU表`:

| id   | title             | price   | spu_id |
| ---- | ----------------- | ------- | ------ |
| 1    | IPhoneX 红色 256G | 8000.00 | 1      |
| 2    | IPhoneX 黑色 128G | 5000.00 | 1      |

`商品规格表`:

| id   | spu_id | name |
| ---- | ------ | ---- |
| 1    | 1      | 颜色 |
| 2    | 1      | 版本 |

`规格选项表`:

| id   | spec_id | name |
| ---- | ------- | ---- |
| 1    | 1       | 黑色 |
| 2    | 1       | 红色 |
| 3    | 2       | 128G |
| 4    | 2       | 256G |

`商品SKU规格信息表`:

| id   | sku_id | spec_id | opt_id |
| ---- | ------ | ------- | ------ |
| 1    | 1      | 1       | 2      |
| 1    | 1      | 2       | 4      |

##### 4. 商品部分-FDFS文件存储系统

文件存储系统需要解决的问题：

​	1）数据冗余。

​	2）线性扩容。

##### 5. 商品部分-Docker使用

1）镜像

| 命令                            | 说明             |
| ------------------------------- | ---------------- |
| docker image pull 组名/镜像名称 | 从仓库拉取镜像   |
| docker image ls                 | 查看本地所有镜像 |
| docker image rm 镜像名称/镜像ID | 删除指定镜像     |

2）容器

| 命令                                                  | 说明               |
| ----------------------------------------------------- | ------------------ |
| docker run [-option] 镜像 [向启动容器中传入的命令]    | 使用镜像创建容器   |
| docker exec -it 容器名或容器id 进入后执行的第一个命令 | 进入指定容器       |
| docker container ls                                   | 查询所有启动的容器 |
| docker container ls --all                             | 查询所有容器       |
| docker container start 容器名称                       | 启动指定容器       |
| docker container stop 容器名称                        | 停止指定容器       |
| docker container rm 容器名称                          | 删除指定容器       |

3）其他

| 命令                               | 说明             |
| ---------------------------------- | ---------------- |
| docker commit 容器名 镜像名        | 将容器保存为镜像 |
| docker save -o 保存的文件名 镜像名 | 将镜像打包为文件 |
| docker load -i ./ubuntu.tar        | 将镜像加载到本地 |

##### 6. 商品部分-自定义文件存储系统

1）自定义文件存储类。

2）修改`DEFAULT_FILE_STORAGE`配置项。