from django import forms
from .models import PurchaseInvoice



class PurchaseInvoiceForm(forms.ModelForm):

    class Meta:
        model = PurchaseInvoice
        fields = ('description', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})