from django.contrib import admin
from .models import User, UserProfile, UserAddress
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'referral_code', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'city', 'is_default', 'created_at')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserAddress, UserAddressAdmin)