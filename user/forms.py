from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username':'Enter your username',
            'first_name':'Enter your first name',
            'last_name':'Enter your last name',
            'email':'Enter your email address',
            'password1':'Enter your password',
            'password2':'Repeat your password'
        }
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','username', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'tagline', 'bio']