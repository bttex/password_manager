from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Sobrescreve o método __init__ para customizar os labels
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'  # Altera o label do campo password1
        self.fields['password2'].label = 'Enter Password Again'  # Altera o label do campo password2

    # Personalizando os widgets para adicionar as classes do Tailwind
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
    }))

class PasswordForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ['site', 'username', 'encrypted_password']
        labels = {
            'site': 'Site',
            'username': 'Username',
            'encrypted_password': 'Password'
        }