from django import template


register=template.Library()





@register.inclusion_tag('info.html',takes_context=True)
def info_list(context):
	return {'data_list':context['data_list'],'header_list':context['header_list']}