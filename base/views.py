from django.shortcuts import render_to_response
from django.template import RequestContext


def inicio(request):
    return render_to_response('base.template.html', {}, context_instance=RequestContext(request))