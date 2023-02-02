from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserNotes, Testimonial

class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'submit-field with-border'
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
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'submit-field with-border'
    class Meta:
        model = User
        fields = ['first_name','username', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'col-auto'})
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'submit-field with-border'
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'tagline']
        labels = {
            'image':'',
        }
       
class UserNotesForm(forms.ModelForm):
    class Meta:
        model = UserNotes
        fields = ['description', 'Priority']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['testimony']