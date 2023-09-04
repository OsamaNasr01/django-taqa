
from django import forms
from .models import Category, Product, Brand, Price, Spec, NumSpecs, TxtSpecs, BoolSpecs




class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'brand', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ('name', 'country', 'description', 'category', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'id': 'brand_name'})
        self.fields['country'].widget.attrs.update({'id': 'brand_country'})
        self.fields['description'].widget.attrs.update({'id': 'brand_description'})
        self.fields['category'].widget.attrs.update({'id': 'brand_category'})
        self.fields['image'].widget.attrs.update({'id': 'brand_image'})



class PriceForm(forms.ModelForm):

    class Meta:
        model = Price
        fields = ('value', 'discount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].label = 'Price'

class SpecForm(forms.ModelForm):
    class Meta:
        model = Spec
        fields = ('name', 'type', 'unit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})


class NumSpecForm(forms.ModelForm):
    class Meta:
        model = NumSpecs
        fields = ('value', )



class TxtSpecForm(forms.ModelForm):
    class Meta:
        model = TxtSpecs
        fields = ('value', )



class BoolSpecForm(forms.ModelForm):
    class Meta:
        model = BoolSpecs
        fields = ('value', )
