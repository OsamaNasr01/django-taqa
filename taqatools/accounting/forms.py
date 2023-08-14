from django import forms
from .models import PurchaseInvoice, CartItem, Offer



class PurchaseInvoiceForm(forms.ModelForm):

    class Meta:
        model = PurchaseInvoice
        fields = ('description', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        
        
class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ('q',)
    
    

class OfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ('user','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})    