
from .models import Question
from django import forms



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'type', 'unit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].label = 'صيغة السؤال:'
        self.fields['type'].label = 'نوع السؤال:'
        self.fields['unit'].label = 'وحدة السؤال إن وجدت:'