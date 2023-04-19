from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AccountInline(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class CustomizedUerAdmin(UserAdmin):

    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUerAdmin)
