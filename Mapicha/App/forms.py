from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo

class RegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','email','password1','password2')
        email =forms.EmailField(required=True)
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title','description', 'image' )
