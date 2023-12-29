from django.contrib import admin
from core.models import *

# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'company', 'status']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['role']


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
