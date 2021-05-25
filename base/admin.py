from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .models import CustomUser,Employee, EmployeeAdditional, Supervisor

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# class SellerAdditionalInline(admin.TabularInline):
#     model = SellerAdditional
class EmployeeAdditionalInline(admin.TabularInline):
    model = EmployeeAdditional
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name','type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# class SellerAdmin(admin.ModelAdmin):
#     inlines = (
#         SellerAdditionalInline,
#     )



class EmployeeAdmin(admin.ModelAdmin):
    inlines = (
        EmployeeAdditionalInline,
    )
admin.site.register(Supervisor)
admin.site.register(Employee, EmployeeAdmin)

#admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)



