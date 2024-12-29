from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('totp/setup/', views.totp_setup, name='totp_setup'),
    path('totp/verify/', views.totp_verify, name='totp_verify'),
    path('passwords/', views.list_passwords, name='list_passwords'),
    path('passwords/add/', views.add_password, name='add_password'),
    path('passwords/edit/<int:pk>/', views.edit_password, name='edit_password'),
    path('passwords/delete/<int:pk>/', views.delete_password, name='delete_password'),
    path('register/', views.register_view, name='register'),
]