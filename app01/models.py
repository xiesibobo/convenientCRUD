from django.db import models

# Create your models here.


class Role(models.Model):
    name=models.CharField(verbose_name='姓名',max_length=32)
    def __str__(self):
        return self.name


class UserInfo(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name