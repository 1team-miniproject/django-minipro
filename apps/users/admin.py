from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    add_form = CustomUserCreationForm

    list_display = ('email', 'name', 'nickname', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email','nickname', 'phone_number')
    readonly_fields = ('last_login',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('name', 'nickname', 'phone_number')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('로그 정보', {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
        'classes' : ('wide'),
        'fields' : ('email', 'password1','password2', 'name', 'nickname', 'phone_number'),
    }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = [fs for fs in fieldsets if fs[0] != '권한']
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ('email', 'is_staff', 'is_superuser')
