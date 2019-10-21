from django.db import models

# Create your models here.
class Userinfo(models.Model):
    id = models.AutoField(primary_key=True)  # 在django中 你可以不指定主键字段 django orm会自动给你当前表新建一个名为id的主键字段
    username = models.CharField(max_length=64)  # 在django orm中 没有char字段  但是django 暴露给用户 可以自定义char字段
    password = models.IntegerField()
    def __str__(self):
        return '我是用户对象:%s'%self.username


class Book(models.Model):
    title = models.CharField(max_length=64)

