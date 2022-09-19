from attr import field
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django import forms
import attr
from django.contrib.auth import get_user_model
User = get_user_model()
# from store import forms


class signupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields= ('username','email','password1','password2')

