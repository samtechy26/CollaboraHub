
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.widgets.TextInput(

            attrs={

                "placeholder": "username",

                "class": "form-control",

            }

        ),

        label="username",
    )
    first_name = forms.CharField(
        widget=forms.widgets.TextInput(

            attrs={

                "placeholder": "First name",

                "class": "form-control",

            }

        ),

        label="First name",

    )
    last_name = forms.CharField(
        widget=forms.widgets.TextInput(

            attrs={

                "placeholder": "last name",

                "class": "form-control",

            }

        ),

        label="last name",
    )
    email = forms.EmailField(
        widget=forms.widgets.EmailInput(

            attrs={

                "placeholder": "Email",

                "class": "form-control",

            }

        ),

        label="Email address",
    )
    password1 = forms.CharField(
        widget=forms.widgets.PasswordInput(

            attrs={

                "placeholder": "Password",

                "class": "form-control",

            }

        ),

        label="password",
    )
    password2 = forms.CharField(
        widget=forms.widgets.PasswordInput(

            attrs={

                "placeholder": "Password Confirmation",

                "class": "form-control",

            }

        ),

        label="Password Confirmation",
    )
    
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'tagline', 'bio']