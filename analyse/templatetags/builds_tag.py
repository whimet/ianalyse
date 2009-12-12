from django import template

register = template.Library()

def more_attention_icon(builds, config):
    build = builds.get(config)
    if build == None :
        return ""

    if build.need_attention() :
        return '<img src="/media/css/img/attention_please.png" alt="latest build passed" title="latest build passed"/>'
    else :
        return ""    
    
def last_build_span(builds):
    build = builds.last()
    if build.is_last_build_old():
        return '<span style="color:red;font-weight:bold">' + build.last_build_t() + "</span>"
    else :
        return '<span>' + build.last_build_t() + "</span>"
            
def last_pass_span(builds):
    build = builds.last()
    if build.is_last_pass_old():
        return '<span style="color:red;font-weight:bold">' + build.last_pass_t() + "</span>"
    else :
        return '<span>' + build.last_pass_t()  + "</span>"   
    
def build_status_icon(builds, config):
    "Display the icon for whether the build pass or not"
    build = builds.get(config)

    if build == None:
        return ''

    if build.is_passed :
        return '<img src="/media/css/img/now_passed.png" alt="latest build passed" title="latest build passed"/>'
    else :
        return '<img src="/media/css/img/now_failed.png" alt="latest build failed" title="latest build failed"/>'

def build_status_class(builds, config):
    "Display the icon for whether the build pass or not"
    build = builds.get(config)

    if build == None:
        return ''

    if build.is_passed :
        return 'now_passed'
    else :
        return 'now_failed'


register.simple_tag(build_status_icon)
register.simple_tag(build_status_class)
register.simple_tag(more_attention_icon)
register.simple_tag(last_pass_span)
register.simple_tag(last_build_span)


