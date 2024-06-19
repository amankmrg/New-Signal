from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Appointment,Doctor
from django.contrib.auth.forms import UserChangeForm
from .forms import RegistrationForm,NewForm



class CustomAdmin(UserAdmin):
    list_display = ('name','email','is_doctor',)
    fieldsets = (
        (None, {'fields': ('password','is_doctor','is_patient','first_name','last_name')}),
        ('Personal info', {'fields': ('email','username')}),
        ('Permissions', {'fields': ('is_staff','is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_patient','is_doctor')}
        ),
    )
    search_fields = ('email',)


# Register your models here.
admin.site.register(CustomUser,CustomAdmin)
admin.site.register(Appointment)
admin.site.register(Doctor)