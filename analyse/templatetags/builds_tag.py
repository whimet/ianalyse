from django import template

register = template.Library()

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

def from_pass_build(builds, config):
    "Display the time between this build the last passed build"
    return 'hha'

def from_last_build(builds, config):
    "Display the time between this build the last build"
    return 'hha'

register.simple_tag(build_status_icon)
register.simple_tag(from_pass_build)
register.simple_tag(from_last_build)
register.simple_tag(build_status_class)



