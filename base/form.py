from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']



class RoomForm(ModelForm):
    class Meta:
        ''' 
            Buy fields of room
        '''
        model = Room
        fields = '__all__' # we can use the list or tuple like that ['name', 'body'] to specify the chosen desired fields
        exclude =   ('host', 'participant') # disiable fields



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
