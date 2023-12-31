from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image']
        widgets = {
            'content': CKEditorWidget(),
        }
        
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})  
        self.fields['content'].widget.attrs.update({'class': 'form-control'})    
        self.fields['image'].widget.attrs.update({'class': 'form-control'})   
        
        self.fields['title'].label = 'عنوان المقال'
        self.fields['category'].label = 'القسم التابع له'
        self.fields['content'].label = 'محتوى المقال'
        self.fields['image'].label = 'صورة المقال'
