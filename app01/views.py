from django.shortcuts import render,redirect,HttpResponse
from utils.pager import Pagination
# Create your views here.
HOST_LIST=[]

from app01 import models


#
# def test(self):
# 	model_list=[]
# 	for i in range(100):
# 		dit={'name':str(i),'email':'rger%s@fdbf.com'%i,'pwd':'123456'}
# 		model_list.append(models.UserInfo(**dit))
# 		models.UserInfo.objects.bulk_create(model_list)
# 	return HttpResponse('OK')
	
for i in range(150):
	HOST_LIST.append('av%s.com'%i)

def hosts(request):
	try:
		current_page=int(request.GET.get('page',1))#获取选择的页码
	except:
		current_page=1
	per_page_count=10#每页选择显示的条数
	start = (current_page - 1 )*per_page_count
	end = current_page * per_page_count
	host_list = HOST_LIST[start:end]
	
	total_count = len(HOST_LIST)
	
	max_page_num,div=divmod(total_count,per_page_count)
	if(div>0) :max_page_num +=1
	page_html_list=[]
	for i in range(1,max_page_num+1):
		temp= '<a class="active" href="/hosts/?page=%s">%s</a>'%(i,i)if i==current_page else  '<a href="/hosts/?page=%s">%s</a>'%(i,i)
		page_html_list.append(temp)
		
	page_html=''.join(page_html_list)
	
	
Book_list=[]
for i in range(1000):
	Book_list.append('白雪公主与%s个小矮人'%i)
	
def book(request):
	pager_obj=Pagination(request.GET.get('page',1),len(Book_list),request.path_info,request.GET)
	book_list = Book_list[pager_obj.start:pager_obj.end]
	html=pager_obj.page_html()
	

	from django.http import QueryDict  # request.GET
	# params = QueryDict(mutable=True)
	
	# request.GET是一个QueryDict类型，
	# 默认不可修改，request.GET._mutable = True
	# request.GET.urlencode() 用于讲k,v构造成URL格式字符串
	# request.GET['page'] = 666
	
	# _list_filter=page%3D5%26id__gt%3D4
	params = QueryDict(mutable=True)
	params['_list_filter'] = request.GET.urlencode()
	list_condition = params.urlencode()
	
	return render(request,'book.html',{'book_list':book_list,'page_html':html,'list_condition':list_condition})



def edit_book(request):
	if request.method=="GET":
		# request.GET['_list_filter']=0
		return render(request,'edit.html')
	else:
		return redirect('/book/?%s'%request.GET.get('_list_filter'))
		