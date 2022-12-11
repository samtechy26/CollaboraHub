from django import forms
from .models import Bid

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

        # def __init__(self, *args, **kwargs):
        #     super(BidForm, self).__init__(*args, **kwargs)
        #     for field in self.fields:
        #         self.fields[field].widget.attrs['class'] = 'bidding-fields'

        
        
        

class ContactForm(forms.Form):
     your_name = forms.HiddenInput()


