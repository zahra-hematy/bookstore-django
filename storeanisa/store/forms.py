# from attr import field
from unicodedata import name
from django import forms
from store.models import *


class ContactUsForm(forms.Form):
    name =forms.CharField()
    email =forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


# class BookRequestForm(forms.ModelForm):
#     class Meta:
#         model = BookRequest
#         fields =['name','author']
        
class BookRequestForm(forms.Form):
    name = forms.CharField()
    author = forms.CharField()
    cover = forms.ImageField(required=False)
