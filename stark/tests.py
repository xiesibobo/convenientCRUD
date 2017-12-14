# from django.test import TestCase
#
# # Create your tests here.
#
#
#
def wapper():
	for i in range(10):
		def inner():
			for j in range(10):
				yield j
		yield inner()
#
#
# for v in wapper():
# 	print('s', v)
#
# 	for k in v :
#
# 		print(k)
#
# data_list = self.model_class.objects.all()
# new_data_list=[]
# for row in data_list:
# 	temp = []
# 	if self.list_display:
# 		for field_name in self.list_display:
# 			if isinstance(field_name, str):
# 				val = getattr(row, field_name)
# 			else:
# 				val = field_name(self, row)
# 			temp.append(val)
# 		new_data_list.append(temp)
# 	else:
# 		#当没有定制显示什么字段时默认显示对象
# 		new_data_list.append([row,])
# return render(request, 'stark/change.html', {'data_list': new_data_list,'header_list':header_list})
#
#
#
#
# def wapper():
# 	for row in data_list:
# 		def inner():
# 			if self.list_display:
# 				for field_name in self.list_display:
# 					if isinstance(field_name, str):
# 						val = getattr(row, field_name)
# 					else:
# 						val = field_name(self, row)
# 					# temp.append(val)
# 					yield val
# 				new_data_list.append(temp)
# 			else:
# 				# 当没有定制显示什么字段时默认显示对象
# 				yield row
# 				# new_data_list.append([row, ])
# 		yield inner()