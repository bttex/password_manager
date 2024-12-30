from django.contrib import admin
from .models import Password

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'username', 'user')
    search_fields = ('service_name', 'username')
    list_filter = ('user',)
