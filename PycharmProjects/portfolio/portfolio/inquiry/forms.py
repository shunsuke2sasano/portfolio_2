from django import forms
from .models import Inquiry, Category

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['category', 'body', 'status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
        }
