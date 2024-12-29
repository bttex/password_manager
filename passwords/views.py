from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import user_has_device
from django.contrib.auth.decorators import login_required, user_passes_test
from passwords.forms import PasswordForm
from django.contrib.auth.forms import UserCreationForm
from passwords.models import Password
from .models import CustomTOTPDevice
import qrcode
from io import BytesIO
from django.http import HttpResponse
import base64
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
import csv

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not user_has_device(user):
                    return redirect('totp_setup')
                return redirect('totp_verify')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def totp_setup(request):
    if request.method == 'POST':
        if 'generate_qr' in request.POST:
            device = CustomTOTPDevice.objects.create(
                user=request.user,
                name='default',
                step=30,  # Configurar para 30 segundos
                t0=0,
                digits=6,
                tolerance=1
            )
            device.confirmed = True
            device.save()

            # Gera QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(device.config_url)
            qr.make(fit=True)

            # Salva QR code como imagem
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            return render(request, 'totp_setup.html', {'qr_code': img_str})
        
        elif 'verify_totp' in request.POST:
            device = CustomTOTPDevice.objects.filter(user=request.user).first()
            totp_code = request.POST.get('totp_code')
            
            if device and device.verify_token(totp_code):
                return redirect('home')
            else:
                return render(request, 'totp_setup.html', {'error': 'Código TOTP inválido'})
    
    return render(request, 'totp_setup.html')

@login_required
def totp_verify(request):
    device = CustomTOTPDevice.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        totp_code = request.POST.get('totp_code')
        
        if device and device.verify_token(totp_code):
            return redirect('home')
        else:
            return render(request, 'totp_verify.html', {'error': 'Invalid TOTP code'})
    
    return render(request, 'totp_verify.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def list_passwords(request):
    passwords = Password.objects.filter(user=request.user)
    return render(request, 'list_passwords.html', {'passwords': passwords})


@login_required
def add_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.user = request.user
            password.save()
            return redirect('list_passwords')
    else:
        form = PasswordForm()
    return render(request, 'add_password.html', {'form': form})


@login_required
def edit_password(request, pk):
    password = get_object_or_404(Password, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PasswordForm(request.POST, instance=password)
        if form.is_valid():
            form.save()
            return redirect('list_passwords')
    else:
        form = PasswordForm(instance=password)
    return render(request, 'edit_password.html', {'form': form})

# ...existing code...

@login_required
def delete_password(request, pk):
    password = get_object_or_404(Password, pk=pk, user=request.user)
    if request.method == 'POST':
        password.delete()
        return redirect('list_passwords')
    return render(request, 'confirm_delete.html', {'password': password})

# ...existing code...

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Função para verificar se o usuário é um administrador
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()  # Pega todos os usuários

    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user_to_delete = get_object_or_404(User, pk=user_id)
            if user_to_delete != request.user:  # Não permitir excluir o próprio usuário
                user_to_delete.delete()
                messages.success(request, f'O usuário {user_to_delete.username} foi excluído com sucesso!')
            else:
                messages.error(request, 'Você não pode excluir seu próprio usuário.')

        elif 'make_admin' in request.POST:
            user_id = request.POST.get('user_id')
            user_to_promote = get_object_or_404(User, pk=user_id)
            if not user_to_promote.is_superuser:
                user_to_promote.is_superuser = True
                user_to_promote.is_staff = True  # Torna o usuário também um "staff"
                user_to_promote.save()
                messages.success(request, f'O usuário {user_to_promote.username} foi promovido a Admin!')
            else:
                messages.warning(request, 'Este usuário já é um Admin.')

        elif 'delete_totp' in request.POST:
            user_id = request.POST.get('user_id')
            user_to_clear_totp = get_object_or_404(User, pk=user_id)

            # Deletar a chave TOTP do usuário
            try:
                # Busca o dispositivo TOTP associado ao usuário
                totp_device = TOTPDevice.objects.get(user=user_to_clear_totp)
                totp_device.delete()  # Deleta o dispositivo TOTP
                messages.success(request, f'A chave TOTP do usuário {user_to_clear_totp.username} foi removida com sucesso!')
            except TOTPDevice.DoesNotExist:
                messages.warning(request, f'O usuário {user_to_clear_totp.username} não tem chave TOTP.')

    return render(request, 'manage_users.html', {'users': users})


@login_required
def export_passwords(request):
    # Obtenha todos os dados de senhas
    passwords = Password.objects.all()

    # Crie a resposta HTTP para o CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="senhas.csv"'

    # Crie o writer para escrever no arquivo CSV
    writer = csv.writer(response)
    
    # Escreva o cabeçalho (os nomes das colunas)
    writer.writerow(['ID', 'Usuário', 'Senha', 'Criado em', 'Modificado em'])  # Customize conforme seus campos

    # Escreva os dados de cada senha
    for password in passwords:
        writer.writerow([password.id, password.user.username, password.password, password.created_at, password.updated_at])  # Customize conforme seus campos

    return response

@login_required
def home(request):
    # Determina se o usuário é admin (superuser ou staff)
    is_admin = request.user.is_superuser or request.user.is_staff
    return render(request, 'home.html', {'is_admin': is_admin})