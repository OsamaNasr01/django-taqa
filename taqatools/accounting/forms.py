from django import forms
from .models import PurchaseInvoice, CartItem, Offer, OfferItem, SaleInvoice, SaleInvoiceItem
from .models import PurchaseInvoice, PurchaseInvoiceItem, Depit, Credit


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
        

class OfferItemForm(forms.ModelForm):

    class Meta:
        model = OfferItem
        fields = ('product','offer', 'q', 'price')

    


class SaleForm(forms.ModelForm):

    class Meta:
        model = SaleInvoice
        fields = ('user','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})    
        

class SaleItemForm(forms.ModelForm):

    class Meta:
        model = SaleInvoiceItem
        fields = ('product','invoice', 'q', 'price')

    



class PurchaseForm(forms.ModelForm):

    class Meta:
        model = PurchaseInvoice
        fields = ('user','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})    
        

class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseInvoiceItem
        fields = ('product','invoice', 'q', 'price')


class DepitForm(forms.ModelForm):

    class Meta:
        model = Depit
        fields = ('description', 'value')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].widget.attrs.update({'class': 'form-control'})    



class CreditForm(forms.ModelForm):

    class Meta:
        model = Credit
        fields = ('description', 'value')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].widget.attrs.update({'class': 'form-control'})   
