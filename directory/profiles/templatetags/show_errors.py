from django import template
register = template.Library()

@register.inclusion_tag('profiles/show_profile_csv_errors.html')
def show_csv_errors(errors_list, title, obj_type):
    class_name = "table-success" if obj_type == "success" else "table-danger"
    return {'errors': errors_list, 'title':title, "class_name":class_name}


@register.filter(name='getkey')
def getkey(value, arg):
    return value.get(arg, "None")