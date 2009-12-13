from django import template

register = template.Library()

def more_attention_icon(project_groups, id):
    build = project_groups.latest_build_of(id)
    
    if build == None :
        return ""

    if build.need_attention() :
        return '<img id="warning_' + id + '" src="/media/css/img/attention_please.png" alt="latest build passed" title="latest build passed"/>'
    else :
        return ""    

def build_status_icon(project_groups, id):
    "Display the icon for whether the build pass or not"
    build = project_groups.latest_build_of(id)

    if build == None:
        return '<img id="now_unknown_' + id + '" src="/media/css/img/now_unknown.png" alt="cannot find log" title="cannot find log"/>'
        
    if build.is_passed :
        return '<img id="now_passed_' + id + '" src="/media/css/img/now_passed.png" alt="latest build passed" title="latest build passed"/>'
    else :
        return '<img id="now_failed_' + id + '" src="/media/css/img/now_failed.png" alt="latest build failed" title="latest build failed"/>'

def last_build_span(builds):
    build = builds.last()
    if build.is_last_build_old():
        return '<span class="last_build_at" style="color:red;font-weight:bold">' + build.last_build_t() + "</span>"
    else :
        return '<span class="last_build_at">' + build.last_build_t() + "</span>"
            
def last_pass_span(builds):
    build = builds.last()
    if build.is_last_pass_old():
        return '<span class="last_pass_at" style="color:red;font-weight:bold">' + build.last_pass_t() + "</span>"
    else :
        return '<span class="last_pass_at">' + build.last_pass_t()  + "</span>"   
    


register.simple_tag(build_status_icon)
register.simple_tag(more_attention_icon)
register.simple_tag(last_pass_span)
register.simple_tag(last_build_span)


