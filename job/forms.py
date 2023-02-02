from django import forms
from .models import Bid, Job, Category

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['Amount','time', 'denom']
        
        labels = {
            'Amount': ('Set your minimal rate'),
            'denom':'',
            'time':'Set your delivery time'
        }
        widgets = {
            'denom': forms.Select(attrs={'class': 'bidding-fields bidding-field'}),
            'time': forms.TextInput(attrs={'class':'bidding-fields bidding-field'}),
            
        }


class JobCreationForm(forms.ModelForm):
    job_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'job_category', 'cost',  'skill', 'description', 'job_file']
        


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Your name"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Your e-mail"
    }))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Subject of email"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your message'
    }))




        