from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from analyse.models import Builds, Build
from analyse.cache import Cache
from analyse.config import *
from django.utils.http import urlquote

def home(request):
    return redirect('/analyse/index.html')

def index(request):
    groups = Groups()
    if (groups.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))
    group_id = request.GET.get('groups', 'default')
    
    if not groups.exists(group_id):
        return redirect('index.html?groups=default')

    configs = groups.find(group_id)    
    results = {'group_id' : group_id, 'configs' : configs, 'project_groups' : Cache.INSTANCE().get_project_group(group_id)}
    return render_to_response('analyse/index.html', Context(results), context_instance = RequestContext(request))

def setup(request):
    groups = Groups()
    if (groups.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))

    current = groups.default().find(request.GET.get('id'))
    results = {"configs" : groups.default(), 'current' : current}
    return render_to_response('analyse/setup.html', Context(results), context_instance = RequestContext(request))

def generate(request) :
    groups = Groups()
    if (groups.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))

    id = request.POST.get('id')
    if id == None:
        Cache.INSTANCE().populate()
    else:
        Cache.INSTANCE().refresh(groups.default().find(id))
    return redirect('index.html')

def show(request):
    groups = Groups()
    if (groups.is_empty()) :
        return render_to_response('analyse/hint.html', Context({}), context_instance = RequestContext(request))
    project_id = request.GET['id']
    config = groups.default().find(project_id)

    if not config.has_result() :
        return redirect('setup.html?id=' + urlquote(project_id))

    builds = Cache.INSTANCE().find(project_id)
    over_all_result = {
        "builds" : builds
    }    
    return render_to_response('analyse/show.html', Context(over_all_result), context_instance = RequestContext(request))

def help(request):
    configs = Groups().default()
    results = {
        "configs" : configs,
    }
    return render_to_response('analyse/help.html', Context(results), context_instance = RequestContext(request))
   
    
    
    
    