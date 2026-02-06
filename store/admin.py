from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Product, Order


# =========================
# Custom User Admin
# =========================
class CustomUserAdmin(UserAdmin):
    """Custom User Admin with superuser creation capability"""

    # Add badge column
    list_display = UserAdmin.list_display + ('is_superuser_badge',)

    # IMPORTANT:
    # We REDEFINE fieldsets instead of appending to avoid duplicates
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Badge display
    def is_superuser_badge(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="background-color:#ff6b6b; color:white; '
                'padding:3px 8px; border-radius:3px; font-weight:bold;">'
                'SUPERUSER</span>'
            )
        return "Staff" if obj.is_staff else "User"

    is_superuser_badge.short_description = 'Admin Status'

    # Admin action
    actions = ['make_superuser']

    def make_superuser(self, request, queryset):
        count = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(
            request,
            f'{count} user(s) were successfully made superuser(s).'
        )

    make_superuser.short_description = "Convert selected users to superuser"


# Unregister default User admin
admin.site.unregister(User)

# Register custom User admin
admin.site.register(User, CustomUserAdmin)


# =========================
# Product Admin
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'price', 'stock', 'is_new')
    list_editable = ('price', 'stock', 'is_new')

    def thumbnail(self, obj):
        if obj.image_main:
            return format_html(
                '<img src="{}" style="width:50px; height:60px; '
                'object-fit:cover; border-radius:4px;" />',
                obj.image_main.url
            )
        return "No Image"

    thumbnail.short_description = "Image"


# =========================
# Order Admin
# =========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'complete', 'created_at')
    list_filter = ('complete', 'created_at')
