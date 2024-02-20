from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import AuthUser


class CustomUserAdmin(UserAdmin):
    model = AuthUser
    list_display = ('phone_number', 'is_staff', 'is_active', 'name', 'email')
    list_filter = ('phone_number', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)


admin.site.register(AuthUser, CustomUserAdmin)

admin.site.site_header = "Backend"
admin.site.site_title = "Backend Admin"
admin.site.index_title = "BoilerPlate"
