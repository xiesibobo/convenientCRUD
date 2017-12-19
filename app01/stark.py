from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from  stark.service import v1
from django.forms import ModelForm

from  app01 import models

'''
自定义显示信息

'''
class UserInfoModelForm(ModelForm):
	class Meta:
		model = models.UserInfo
		
		fields='__all__'
		error_messages={
			'name':{
				'required':'用户名不能为空'
			}
		}


class UserInfoConfig(v1.StarkConfig):
	def extra_url(self):
		url_list = [
			url(r'^sss/$', self.func)
		]
		return url_list
	
	def func(self, request):
		return HttpResponse('OK')

	
	list_display = [ 'id', 'name','email','ut']
	
	show_add_btn = True
	'''
	使用自定义的modelform
	自定义的错误提示信息
	'''
	model_form_class = UserInfoModelForm


# v1.site.register(models.UserInfo)
v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role)
