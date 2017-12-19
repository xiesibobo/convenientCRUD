from django.db import models

# Create your models here.
class UserType(models.Model):
    title = models.CharField(verbose_name='类型名称',max_length=32)

    def __str__(self):
        return self.title

class Role(models.Model):
    name=models.CharField(verbose_name='名字',max_length=32)
    
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    name=models.CharField(verbose_name='姓名',max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    pwd = models.CharField(verbose_name='密码', max_length=32)
    ut = models.ForeignKey(verbose_name='用户类型', to="UserType", default=1)
    def __str__(self):
        return self.name