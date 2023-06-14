from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'is_superuser', 'is_staff')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('id', 'email', 'name')

admin.site.register(User, UserAdmin)


