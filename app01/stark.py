from django.conf.urls import url
from django.shortcuts import HttpResponse,redirect
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
	model_form_class = UserInfoModelForm
	show_search_form = True
	search_field = ['name__contains','email__contains']
	#
	'''
	使用自定义的modelform
	自定义的错误提示信息
	'''
	
	show_actions = True
	def multi_del(self,request):
		
		pk_list = request.POST.getlist('pk')
		print('pk_list',pk_list)
		self.model_class.objects.filter(id__in=pk_list).delete()
		reurl = self.get_list_url()
		if request.GET.urlencode():
			reurl=reurl + '?' + request.GET.urlencode()
		return redirect(reurl)
	multi_del.short_desc="批量删除"
	actions = [multi_del]
	

# v1.site.register(models.UserInfo)
v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role)
