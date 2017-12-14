
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from  stark.service import v1

from  app01 import models



class UserInfoConfig(v1.StarkConfig):
    def checkbox(self,obj):
        return mark_safe('<input type="checkbox" name="pk" value="%s">'%(obj.id))

    def edit(self):
        return mark_safe('<a href="/edit/%s">编辑</a>')

v1.site.register(models.UserInfo)
v1.site.register(models.Role)
