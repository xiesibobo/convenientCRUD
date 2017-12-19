# convenientCRUD

2017年12月14日16:37:55
>完成模仿在前端显示对象和显示对象字段的定制

>写完相关功能，自定义视图，自动添加选择增加删除，用户自定义显示字段

>反向生成url

>生成class 使用type



<table>
    <tr>
        <td>Foo</td>
        <td>Foo</td>
    </tr>
     <tr>
        <td>Foo</td>
        <td>Foo</td>
    </tr>
</table>



# 封装继承多态

<ol>
<li>

>封装
    <ul>
    <li>数据封装</li>
    <li>封装方法和属性（将一类属性封装到一个类中）</li>
    </ul>
</li>
<li>

>继承
>>多继承，左继承优先

</li>
<li>

>生成器
>>*在django中需要进行二次循环的时候，在进行展示时，需要使用form和modelform进行加工时*

</li>
</ol>

#分页器，*2017年12月18日09:20:19*

<pre>
<code>
	from django.http import QueryDict  # request.GET
	# params = QueryDict(mutable=True)
	
	# request.GET是一个QueryDict类型，
	# 默认不可修改，request.GET._mutable = True
	# request.GET.urlencode() 用于将k,v构造成URL格式字符串格式化
	# request.GET['page'] = 666
	
	# _list_filter=page%3D5%26id__gt%3D4
	params = QueryDict(mutable=True)
	params['_list_filter'] = request.GET.urlencode()
	list_condition = params.urlencode()
</code>
</pre>

####保存跳转到添加或者修改页面前页面的条件


<ol>
<li>

>第一种方式
<pre>
<code>
list_condition = request.GET.urlencode()
直接拼接
</code>
</pre>
</li>
<li>

>第二种方式
<pre>
<code>
params = QueryDict(mutable=True)
params['_list_filter'] = request.GET.urlencode()
list_condition = params.urlencode()
</code>
</pre>
<pre><code>
def edit_host(request,pk):
if request.method == "GET":
    return render(request,'edit_host.html')
else:
    # 修改成功 /hosts/?page=5&id__gt=4
    url = "/hosts/?%s" %(request.GET.get('_list_filter'))
    return redirect(url)
</code></pre>
</li>
</ol>

>在获取url和生成url时传入request对象，利用对象生成url的参数
#2017年12月19日08:35:16
- 整合代码