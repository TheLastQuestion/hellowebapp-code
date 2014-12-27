from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import slugify

from collection.models import Thing
from collection.forms import ThingForm


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


@login_required
def edit_thing(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)

    # grab the current logged in user and make sure they're the owner of the thing
    user = request.user
    if thing.user != user:
        raise Http404

    # set the form we're using...
    form_class = ThingForm

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


def create_thing(request):
    # request.user is the logged in user, we're going to assign it to "user" to make it easy
    user = request.user

    form_class = ThingForm

    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            # create the slug from our name
            slug = slugify(name)

            # create our object
            thing = Thing.objects.create(
                name=name,
                description=description,
                slug=slug,
                user=user,
            )

        # redirect to our newly created thing
        return redirect('thing_detail', slug=thing.slug)

    # otherwise just create the form
    else:
        form = form_class()

    return render_to_response('things/create_thing.html', {
        'form': form,
    }, context_instance=RequestContext(request))
