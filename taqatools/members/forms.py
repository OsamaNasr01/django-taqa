from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Company, CoCategory, Details, Account, Gov, City, Address

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'رقم التليفون'
        self.fields['username'].help_text = 'ادخل رقم الواتس اب الخاص بك'
        self.fields['first_name'].label = 'الاسم الاول'
        self.fields['last_name'].label = 'الاسم الاخير'
        self.fields['email'].label = 'البريد الاليكتروني'
        self.fields['password1'].label = 'رمز الدخول السري'
        self.fields['password2'].label = 'تأكيد رمز الدخول السري'
        self.fields['password2'].help_text = 'ادخل نفس الرمز الذي ادخلته من قبل للتأكيد'


class AddCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'description', 'image', 'phone', 'email', 'website', 'address', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['name'].label = 'اسم الشركة'
        self.fields['description'].label = 'نبذة عن الشركة'
        self.fields['image'].label = 'لوجو الشركة'
        self.fields['phone'].label = 'رقم التليفون'
        self.fields['email'].label = 'البريد الاليكتروني'
        self.fields['website'].label = 'موقع الويب'
        self.fields['address'].label = 'عنوان الشركة'
        self.fields['category'].label = 'تخصص الشركة'






class AddCoCategoryForm(forms.ModelForm):

    class Meta:
        model = CoCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'اسم التخصص'
        self.fields['description'].label = 'نبذة عن التخصص'
  
  
        
class DetailsForm(forms.ModelForm):

    class Meta:
        model = Details
        fields = "__all__"


        
class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = "__all__"






class AddGovForm(forms.ModelForm):

    class Meta:
        model = Gov
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'اسم المحافظة'






class AddCityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('name', 'gov')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['gov'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'اسم المدينة'
        self.fields['gov'].label = 'المحافظة التابعة لها'




class AddAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('details',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['details'].widget.attrs.update({'class': 'form-control'})
        self.fields['details'].label = 'العنوان بالتفصيل'
  