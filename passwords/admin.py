from django.contrib import admin
from .models import Password

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('site', 'username', 'user')
    search_fields = ('site', 'username')
    list_filter = ('user',)
