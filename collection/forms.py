from django.forms import ModelForm
from collection.models import Thing

class EditThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ('name', 'description',)
