from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    ordering = ('username',)  # Order by username by default, but you can change this
    search_fields = ('username', 'email')  # Allow searching by username and email
    actions = None  # Remove the default actions
    # fields = ('username', 'email', 'is_active')  # Only show these fields in the edit form

# Unregister the original User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
