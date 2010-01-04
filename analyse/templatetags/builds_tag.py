from django import template

register = template.Library()

def more_attention_icon(project_groups, id):
    build = project_groups.latest_build_of(id)
    
    if build == None :
        return ""

    if build.need_attention() :
        return '<img id="warning_' + id + '" src="/media/css/img/attention_please.png" alt="you may need to pay attention on this build" title="you may need to pay attention on this build"/>'
    else :
        return ""    

def build_status_icon(project_groups, id):
    "Display the icon for whether the build pass or not"
    build = project_groups.latest_build_of(id)

    if build == None:
        return '<img id="now_unknown_' + id + '" src="/media/css/img/now_unknown.png" alt="cannot read the log files" title="cannot find log"/>'
        
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

def total_runs(builds):
    return str(builds.total_count()) + '(s)'

def avg_build_time(builds):
    return str(builds.avg_build_time())  + '(s)'

def project_id(builds):
    return builds.project_id()

def pass_rate(builds):
    return  "%.2f%%" % (builds.pass_rate() * 100)

def summary(builds):
    return str(builds.total_count()) + ' runs between ' + str(builds.started_at()) + " and " + str(builds.ended_at())

def group_selection(groups, group_id):
    selection_box = '<select id="group_selection_box">'
    options = ''
    for group in groups:
        options = options + '<option id="' + group.id + '" value="' + group.id + '"'
        if group_id == group.id:
            options = options + ' selected="selected" '
        options =  options + '>' + group.id + "</option>"
    selection_box = selection_box + options + '</select>'
    return selection_box

def group_cmp(url, configs, group_id):
    width="400"
    height="320"
    if len(configs) > 5:
        width = 900
    return '''<script type="text/javascript">
        swfobject.embedSWF(
                "%(url)s/swf/open-flash-chart.swf", "projects_comparation", "%(width)s", "%(height)s",
                "9.0.0", "expressInstall.swf",
        {"data-file":"/results/group_%(group_id)s_comparation.txt"}
                );
    </script>''' % \
    {'width': width, "height": height, "group_id":group_id, 'url':url}
    

register.simple_tag(total_runs)
register.simple_tag(avg_build_time)
register.simple_tag(project_id)
register.simple_tag(pass_rate)
register.simple_tag(summary)
register.simple_tag(build_status_icon)
register.simple_tag(more_attention_icon)
register.simple_tag(last_pass_span)
register.simple_tag(last_build_span)
register.simple_tag(group_selection)
register.simple_tag(group_cmp)
