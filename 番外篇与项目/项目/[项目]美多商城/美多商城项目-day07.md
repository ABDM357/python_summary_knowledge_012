### 美多商城项目

##### 富文编辑器

什么富文本？带有格式的文本。

##### 首页

商品分类: 查询1次数据库

广告信息：查询1次数据库

每个用户访问商品首页时，都需要查询2次数据库。

假如1分钟1000个用户访问网站的首页，查询了2000次数据库。

##### 网站优化

1）缓存：将获取到的数据直接放到缓存中，再来用户进行访问的时候，直接从缓存中获取结果返回。

2）页面静态化：

​	将页面用到的数据从数据库中查询出来，然后生成一个静态页面，当其他用户来访问时，直接返回静态页面。

3）页面静态化步骤：

​	a）根据对应的页面准备好一个模板文件，在模板文件把所需的数据及怎么进行展示写好。	

​	b）从数据库中查询页面所需的数据，然后调用模板进行模板渲染，获取替换之后的内容。

​	c）将替换之后内容保存成一个静态文件。

4）静态化页面更新(静态页面内容和数据库中数据保持同步)

​	a）定时任务: 页面内容更新比较频繁，每隔一段时间自动调用生成静态文件函数，重新生成静态页面。

​	b）针对内容更新不频繁页面，当Admin修改了指定数据的时，再重新生成对应的静态页面。

##### 商品详情页静态化

把网站中每个商品都生成一个对应的静态页面，当用户访问指定的商品时，直接返回对应的静态页面。

##### Admin修改表数据

当管理员通过Admin修改某个表数据的时候，表对应模型类对应Admin管理类中`save_model`和`delete_model`会被调用。新增或更新时调`save_model`，删除时调用`delete_model`.



