from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import user_has_device
from django.contrib.auth.decorators import login_required
from passwords.forms import PasswordForm
from django.contrib.auth.forms import UserCreationForm
from passwords.models import Password
from .models import CustomTOTPDevice

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
    if user_has_device(request.user):
        return redirect('home')
    
    device = CustomTOTPDevice.objects.filter(user=request.user).first()
    if not device:
        device = CustomTOTPDevice.objects.create(
            user=request.user, 
            name='default',
            step=60,
            t0=0,
            digits=6,
            tolerance=0
        )
        device.save()
    
    if request.method == 'POST':
        totp_code = request.POST.get('totp_code')
        if device.verify_token(totp_code):
            device.confirmed = True
            device.save()
            return redirect('home')
    
    # Gerar QR code
    import qrcode
    import qrcode.image
    import base64
    from io import BytesIO
    
    # Criar QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(device.config_url)
    qr.make(fit=True)
    
    # Converter para imagem base64
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code = base64.b64encode(buffered.getvalue()).decode()
    
    return render(request, 'totp_setup.html', {
        'device': device,
        'qr_code': f"data:image/png;base64,{qr_code}"
    })

@login_required
def totp_verify(request):
    device = TOTPDevice.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        totp_code = request.POST.get('totp_code')
        if device and device.verify_token(totp_code):
            return redirect('home')
    
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
    return render(request, 'delete_password.html', {'password': password})

# ...existing code...

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Especificar o backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('totp_setup')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})