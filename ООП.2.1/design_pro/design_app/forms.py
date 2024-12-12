from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Request, Category

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label='ФИО')
    email = forms.EmailField(label='Email')
    agree_terms = forms.BooleanField(label='Согласие на обработку персональных данных')

    class Meta:
        model = CustomUser
        fields = ('full_name', 'username', 'email', 'password1', 'password2', 'agree_terms')

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'description', 'category', 'image')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)