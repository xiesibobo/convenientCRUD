from django.conf.urls import url
from django.shortcuts import HttpResponse, render


class StarkConfig(object):
	list_display = []
	# 默认为空，则显示为空
	def __init__(self, model_class, site):
		self.model_class = model_class
		self.site = site
		
	
	def geturls(self):
		
		app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
		url_patterns = [
			url(r'^$', self.changelist_view, name='%s_%s_changelist' % app_model_name),
			url(r'^add$', self.add_view, name='%s_%s_add' % app_model_name),
			url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % app_model_name),
			url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
		]
		return url_patterns
	
	@property
	def urls(self):
		return self.geturls()
	
	def changelist_view(self, request, *args, **kwargs):
		header_list=[]
		for field_name in self.list_display:
			if isinstance(field_name,str):
				verbose_name=self.model_class._meta.get_field(field_name).verbose_name
			else:
				verbose_name=field_name(self,is_header=True)
			header_list.append(verbose_name)
		
		
		
		# 当有自定义的显示内容时
		data_list = self.model_class.objects.all()
		new_data_list=[]
		for row in data_list:
			temp = []
			if self.list_display:
				for field_name in self.list_display:
					if isinstance(field_name, str):
						val = getattr(row, field_name)
					else:
						val = field_name(self, row)
					temp.append(val)
				new_data_list.append(temp)
			else:
				#当没有定制显示什么字段时默认显示对象
				new_data_list.append([row,])
		return render(request, 'stark/change.html', {'data_list': new_data_list,'header_list':header_list})
	
	# def  changelist_view(self,request,*args,**kwargs):
	#     return HttpResponse('列表')
	def add_view(self, request, *args, **kwargs):
		return HttpResponse('添加')
	
	def delete_view(self, request, *args, **kwargs):
		return HttpResponse('删除')
	
	def change_view(self, request, *args, **kwargs):
		return HttpResponse('修改')


class StarkSite(object):
	def __init__(self):
		self._registry = {}
	
	def register(self, model_class, stark_config_class=None):
		if not stark_config_class:
			stark_config_class = StarkConfig
		
		self._registry[model_class] = stark_config_class(model_class, self)
	
	@property
	def urls(self):
		return (self.geturls(), None, 'stark')
	
	def geturls(self):
		url_pattern = []
		for model_class, stark_config_obj in self._registry.items():
			'''
			为每个类创建四个url
			'''
			app_name = model_class._meta.app_label
			model_name = model_class._meta.model_name
			
			curd_url = url(r'^%s/%s/' % (app_name, model_name), (stark_config_obj.urls, None, None))
			url_pattern.append(curd_url)
		
		return url_pattern


site = StarkSite()
