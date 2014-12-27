from django.shortcuts import render, render_to_response
from django.template import RequestContext
from collection.models import Thing
from collection.forms import EditThingForm

# the rewritten view!
def index(request):
    things = Thing.objects.all()
    return render_to_response('index.html', {
        'things': things,
    }, context_instance=RequestContext(request))

def thing_detail(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)
    # and pass to the template
    return render_to_response('things/thing_detail.html', {
        'thing': thing,
    }, context_instance=RequestContext(request))

def edit_thing(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)
    # set the form we're using...
    form_class = EditThingForm

    # if we're coming to this view from a submitted form,  
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('thing_detail', slug=thing.slug)
    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # and render the template
    return render_to_response('things/edit_thing.html', {
        'thing': thing,
        'form': form,
    }, context_instance=RequestContext(request))
