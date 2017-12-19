"""
自定义分页组件的使用方法：
    pager_obj = Pagination(request.GET.get('page',1),len(HOST_LIST),request.path_info,request.GET)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request,'hosts.html',{'host_list':host_list,"page_html":html})
"""


class Pagination(object):
	"""
	自定义分页
	"""
	
	def __init__(self, current_page, total_count, base_url, params, per_page_count=10, max_pager_count=11):
		try:
			current_page = int(current_page)
		except Exception as e:
			current_page = 1
		if current_page <= 0:
			current_page = 1
		self.current_page = current_page
		# 数据总条数
		self.total_count = total_count
		
		# 每页显示10条数据
		self.per_page_count = per_page_count
		
		# 页面上应该显示的最大页码
		max_page_num, div = divmod(total_count, per_page_count)
		if div:
			max_page_num += 1
		self.max_page_num = max_page_num
		
		# 页面上默认显示11个页面（当前页在中间）
		self.max_pager_count = max_pager_count
		self.half_max_pager_count = int((max_pager_count - 1) / 2)
		
		# URL前缀
		self.base_url = base_url
		
		# request.GET
		import copy
		params = copy.deepcopy(params)
		params._mutable = True
		# 包含当前列表页面所有的搜索条件
		# {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
		# self.params[page] = 8
		# self.params.urlencode()
		# source=2&status=2&gender=2&consultant=1&page=8
		# href="/hosts/?source=2&status=2&gender=2&consultant=1&page=8"
		# href="%s?%s" %(self.base_url,self.params.urlencode())
		self.params = params
	
	@property
	def start(self):
		# 每一次请求起始页码
		return (self.current_page - 1) * self.per_page_count
	
	@property
	def end(self):
		# 每一次请求理想末尾页码
		return self.current_page * self.per_page_count
	
	def page_html(self):
		# 如果总页数 <= 11
		if self.max_page_num <= self.max_pager_count:
			pager_start = 1
			pager_end = self.max_page_num
		# 如果总页数 > 11
		else:
			# 如果当前页 <= 5
			if self.current_page <= self.half_max_pager_count:
				pager_start = 1
				pager_end = self.max_pager_count
			else:
				# 当前页 + 5 > 总页码
				if (self.current_page + self.half_max_pager_count) > self.max_page_num:
					pager_end = self.max_page_num
					pager_start = self.max_page_num - self.max_pager_count + 1
				else:
					pager_start = self.current_page - self.half_max_pager_count
					pager_end = self.current_page + self.half_max_pager_count
		
		page_html_list = []
		page_html_list.append('<nav aria-label="Page navigation"><ul class="pagination">')
		# {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
	
		
		self.params['page'] = 1
		first_page = '<li><a  href="%s?%s">首页</a></li>' % (self.base_url, self.params.urlencode(),)
		page_html_list.append(first_page)
		# 首页
		
		# 上一页
		previous_num = self.current_page - 1
		self.params['page'] = previous_num
		if previous_num > 0:
			previous = '<li><a href="%s?%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (
				self.base_url, self.params.urlencode())
		else:
			previous = '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
		page_html_list.append(previous)
		
		for i in range(pager_start, pager_end + 1):
			self.params['page'] = i
			if i == self.current_page:
				temp = '<li class="active"><a class="" href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i,)
			else:
				temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i,)
			page_html_list.append(temp)
		

		
		# 下一页
		next_num = str(self.current_page + 1) if self.current_page + 1<= self.max_page_num else '#'
		self.params['page'] = next_num
		next_header = '<li'
		if not next_num.isdigit():
			next_header='<li'+' class="disabled"'
		next_page=next_header+'><a href="%s?%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'%(self.base_url,self.params.urlencode())
		page_html_list.append(next_page)
		self.params['page'] = self.max_page_num
		last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, self.params.urlencode(),)
		page_html_list.append(last_page)
		page_html_list.append('</ul></nav>')
		return ''.join(page_html_list)
