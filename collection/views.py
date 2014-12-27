from django.shortcuts import render, render_to_response
from django.template import RequestContext


def index(request):
    number = 6
    # don't forget the quotes because it's a string, not an integer
    thing = "Thing name"
    return render_to_response('index.html', {
        'number': number,
        # don't forget to pass it in, and the last comma
        'thing': thing,
    }, context_instance=RequestContext(request))
