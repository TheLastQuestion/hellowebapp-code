from django.shortcuts import render, render_to_response
from django.template import RequestContext
from collection.models import Thing

# the rewritten view!
def index(request):
    things = Thing.objects.all()
    return render_to_response('index.html', {
        'things': things,
    }, context_instance=RequestContext(request))
