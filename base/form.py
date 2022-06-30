from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        ''' Buy fields of room'''
        model = Room
        fields = '__all__' # we can use the list or tuple like that ['name', 'body'] to specify the chosen desired fields
        exclude =   ('host', 'participant') # disiable fields