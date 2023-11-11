from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')