from django.contrib import admin
from .models import Password

class PasswordAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'login', 'user', 'created_at', 'updated_at')

admin.site.register(Password, PasswordAdmin)
