
from django import forms
from .models import PumpOfferRequest, PumpOfferItem, PumpOffer




class PumpOfferRequestForm(forms.ModelForm):

    class Meta:
        model = PumpOfferRequest
        fields = ('hp', 'gwdepth', 'boreholediam', 'irrigation', 'power',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hp'].widget.attrs.update({'class': 'form-control'})
        self.fields['gwdepth'].widget.attrs.update({'class': 'form-control'})
        self.fields['boreholediam'].widget.attrs.update({'class': 'form-control'})
        self.fields['irrigation'].widget.attrs.update({'class': 'form-control'})
        self.fields['power'].widget.attrs.update({'class': 'form-control'})
        self.fields['hp'].label = ' قدرة الطلمبة الغاطسة بالحصان'
        self.fields['gwdepth'].label = 'عمق وش المياه من سطح الارض بالمتر'
        self.fields['boreholediam'].label = 'قطر ماسورة البير بالبوصة'
        self.fields['irrigation'].label = 'نوع نظام الري'
        self.fields['power'].label = 'مصدر الكهرباء'
        
        



class TermsForm(forms.ModelForm):

    class Meta:
        model = PumpOffer
        fields = ('valid', 'include_taxes', 'include_trans', 'installment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valid'].widget.attrs.update({'class': 'form-control'})
        # self.fields['include_taxes'].widget.attrs.update({'class': 'form-control'})
        # self.fields['include_trans'].widget.attrs.update({'class': 'form-control'})
        # self.fields['installment'].widget.attrs.update({'class': 'form-control'})
        
        


