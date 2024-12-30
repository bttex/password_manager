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
        fields = ['service_name', 'username', 'encrypted_password']
        labels = {
            'service_name': 'Nome do Serviço',
            'username': 'Login',
            'encrypted_password': 'Senha'
        }

    def save(self, commit=True):
        instance = super().save(commit=False)  # Cria a instância do objeto sem salvar no banco ainda
        instance.service_name = self.cleaned_data['site']  # Garante que o campo 'site' seja salvo
        instance.username = self.cleaned_data['username']  # Garante que o campo 'username' seja salvo
        raw_password = self.cleaned_data['encrypted_password']
        instance.set_password(raw_password)  # Criptografa a senha antes de salvar
        if commit:
            instance.save()  # Salva o objeto no banco de dados
        return instance  # Correção do erro de digitação
    
    
    
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise ValidationError('O nome de usuário não pode conter espaços.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('As senhas não coincidem.')
        return password2