from django import template
  
register = template.Library()
  
@register.filter()
def get_child_values(parameter_values, parameter):
    return parameter_values.filter(param=parameter.id)
