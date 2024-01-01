
from django import forms
from .models import Category, Product, Brand, Price, Spec, Choice




class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['name'].label = 'اسم القسم'
        self.fields['description'].label = 'وصف القسم'
        self.fields['image'].label = 'صورة القسم'
        


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'brand' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['name'].label = 'اسم المنتج'
        self.fields['description'].label = 'وصف المنتج'
        self.fields['image'].label = 'صورة المنتج'
        self.fields['brand'].label = 'الشركة المصنعة للمنتج'


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
        
        self.fields['name'].label = 'اسم البراند'
        self.fields['description'].label = 'وصف البراند'
        self.fields['image'].label = 'لوجو البراند'
        self.fields['country'].label = 'جنسية  البراند'
        self.fields['category'].label = 'القسم التابع له البراند'



class PriceForm(forms.ModelForm):

    class Meta:
        model = Price
        fields = ('value', 'discount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control'})
        self.fields['value'].label = 'السعر'
        self.fields['discount'].label = 'نسبة الخصم %'

class SpecForm(forms.ModelForm):
    class Meta:
        model = Spec
        fields = ('name', 'type', 'unit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'اسم الخاصية'
        self.fields['type'].label = 'نوع الخاصية'
        self.fields['unit'].label = 'وحدة الخاصية'




class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].label = 'نص الاختيار:'