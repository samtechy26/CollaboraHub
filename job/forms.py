from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['Amount','time', 'denom']

class ContactForm(forms.Form):
     your_name = forms.HiddenInput()