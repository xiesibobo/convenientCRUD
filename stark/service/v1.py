from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm

from utils.pager import Pagination
from django.http import QueryDict


class ChangeList(object):
	def __init__(self, config, queryset):
		self.config = config
		self.list_display = config.get_list_display()
		self.model_class = config.model_class
		self.request = config.request
		current_page = self.request.GET.get('page', 1)
		total_count = queryset.count()
		page_obj = Pagination(current_page=current_page, total_count=total_count, base_url=self.request.path_info,
		                      params=self.request.GET, per_page_count=20)
		self.page_obj = page_obj
		self.data_list = queryset[page_obj.start:page_obj.end]
	
	def head_list(self):
		'''
		构造表头
		:return:
		'''
		result = []
		for field_name in self.list_display:
			if isinstance(field_name, str):
				verbose_name = self.model_class._meta.get_field(field_name).verbose_name
			else:
				verbose_name = field_name(self.config, is_header=True)
			
			result.append(verbose_name)
		return result
	
	def body_list(self):
		new_data_list = []
		for row in self.data_list:
			temp = []
			if self.list_display:
				for field_name in self.model_class.get_list_display():
					if isinstance(field_name, str):
						val = getattr(row, field_name)
					else:
						val = field_name(self, row)
					temp.append(val)
				new_data_list.append(temp)
		return new_data_list


class StarkConfig(object):
	def checkbox(self, obj=None, is_header=False):
		if is_header:
			return '选择'
		return mark_safe('<input type="checkbox" name="pk" value="%s">' % (obj.id))
	
	def edit(self, obj=None, is_header=False):
		if is_header:
			return '操作'
		params = QueryDict(mutable=True)
		params[self._query_param_key] = self.request.GET.urlencode()
		list_condition = params.urlencode()
		
		return mark_safe('<a href="%s?%s">编辑</a>' % (self.get_change_url(obj.id), list_condition))
	
	def delete(self, obj=None, is_header=False):
		if is_header:
			return '操作'
		return mark_safe('<a href="%s">删除</a>' % (self.get_delete_url(obj.id),))
	
	list_display = []
	
	def get_list_display(self):
		data = []
		if self.list_display:
			data.extend(self.list_display)
			data.append(StarkConfig.edit)
			data.append(StarkConfig.delete)
			data.insert(0, StarkConfig.checkbox)
		
		return data
	
	show_add_btn = False
	
	def get_show_add_btn(self):
		return self.show_add_btn
	
	# 默认为空，则显示为空
	def __init__(self, model_class, site):
		self.model_class = model_class
		self.site = site
		self.request = None
		self._query_param_key = '_listfilter'
	
	def wapper(self, view_func):
		def inner(request, *args, **kwargs):
			self.request = request
			
			return view_func(*args, **kwargs)
		
		return inner
	
	def geturls(self):
		
		app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
		url_patterns = [
			url(r'^$', self.wapper(self.changelist_view), name='%s_%s_changelist' % app_model_name),
			url(r'^add$', self.wapper(self.add_view), name='%s_%s_add' % app_model_name),
			url(r'^(\d+)/change/$', self.wapper(self.change_view), name='%s_%s_change' % app_model_name),
			url(r'^(\d+)/delete/$', self.wapper(self.delete_view), name='%s_%s_delete' % app_model_name),
		]
		url_patterns.extend(self.extra_url())
		return url_patterns
	
	def extra_url(self):
		'''
		钩子，目的是能够实现扩展url
		:return:
		'''
		return []
	
	@property
	def urls(self):
		return self.geturls()
	
	def get_change_url(self, nid):
		
		name = "stark:%s_%s_change" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
		edit_url = reverse(name, args=(nid,))
		return edit_url
	
	def get_list_url(self, ):
		
		name = "stark:%s_%s_changelist" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
		edit_url = reverse(name)
		return edit_url
	
	def get_add_url(self):
		name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
		edit_url = reverse(name)
		return edit_url
	
	def get_delete_url(self, nid):
		name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
		edit_url = reverse(name, args=(nid,))
		return edit_url
	
	def changelist_view(self, *args, **kwargs):
		data_list = self.model_class.objects.all()
		cls = ChangeList(self, data_list)
		header_list = []
		for field_name in self.get_list_display():
			if isinstance(field_name, str):
				verbose_name = self.model_class._meta.get_field(field_name).verbose_name
			else:
				verbose_name = field_name(self, is_header=True)
			header_list.append(verbose_name)
		# header_list=cls.head_list()
		
		# 当有自定义的显示内容时
		
		pager_obj = Pagination(self.request.GET.get('page', 1), data_list.count(), self.request.path_info,self.request.GET)
		
		new_data_list = []
		for row in data_list[pager_obj.start:pager_obj.end]:
			temp = []
			if self.list_display:
				for field_name in self.get_list_display():
					if isinstance(field_name, str):
						val = getattr(row, field_name)
					else:
						val = field_name(self, row)
					temp.append(val)
				new_data_list.append(temp)
			else:
				# 当没有定制显示什么字段时默认显示对象
				new_data_list.append([row, ])
		html = pager_obj.page_html()
		
		# 记录下参数
		
		params = QueryDict(mutable=True)
		params[self._query_param_key] = self.request.GET.urlencode()
		list_condition = params.urlencode()
		
		return render(self.request, 'stark/change.html', {'data_list': new_data_list, 'header_list': header_list,'add_url': self.get_add_url()+'?'+list_condition,'show_add_btn': self.get_show_add_btn(),'html': html, })
	
	# def  changelist_view(self,request,*args,**kwargs):
	#     return HttpResponse('列表')
	model_form_class = None
	
	def get_model_form_class(self):
		if self.model_form_class:
			return self.model_form_class
		
		class TestModelForm(ModelForm):
			class Meta:
				model = self.model_class
				fields = "__all__"
		
		Meta = type('Meta', (object,), {'model': self.model_class, 'fields': '__all__'})
		TestModelForm = type('TestModelForm', (ModelForm,), {'Meta': Meta})
		return TestModelForm
	
	def add_view(self, *args, **kwargs):
		'''
		自定义错误信息，默认显示英文
		使用get_model_form_class
		:param request:
		:param args:
		:param kwargs:
		:return:
		'''
		model_form_class = self.get_model_form_class()
		if self.request.method == "GET":
			
			form = model_form_class()
			return render(self.request, 'stark/add_view.html', {'form': form})
		else:
			form = model_form_class(self.request.POST)
			if form.is_valid():
				form.save()
				return redirect(self.get_list_url() + "?" + self.request.GET.get(self._query_param_key))
			return render(self.request, 'stark/add_view.html', {'form': form})
	
	def delete_view(self, request, nid, *args, **kwargs):
		self.model_class.objects.filter(pk=nid).delete()
		return redirect(self.get_list_url())
	
	def change_view(self, request, nid, *args, **kwargs):
		change_obj = self.model_class.objects.filter(pk=nid).first()
		if not change_obj:
			redirect(self.get_list_url())
		model_form_class = self.get_model_form_class()
		if request.method == "GET":
			form = model_form_class(instance=change_obj)
		elif request.method == "POST":
			form = model_form_class(instance=change_obj, data=request.POST)
			if form.is_valid():
				form.save()
				reurl = self.get_list_url() + "?" + request.GET.get(self._query_param_key)
				print(reurl)
				return redirect(reurl)
		return render(request, 'stark/change_view.html', {'form': form})


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
