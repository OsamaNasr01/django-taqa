
from django import forms
from .models import PumpOfferRequest, PumpOfferItem




class PumpOfferRequestForm(forms.ModelForm):

    class Meta:
        model = PumpOfferRequest
        fields = ('hp', 'gwdepth', 'boreholediam',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hp'].widget.attrs.update({'class': 'form-control'})
        self.fields['gwdepth'].widget.attrs.update({'class': 'form-control'})
        self.fields['boreholediam'].widget.attrs.update({'class': 'form-control'})
        
        


