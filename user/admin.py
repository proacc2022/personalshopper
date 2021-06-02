from django.contrib import admin
from django.contrib import admin
# Need to import this since auth models get registered on import.
import django.contrib.auth.admin
import django.contrib.auth.models
# Register your models here.
from user.models import *
from django.contrib import auth

class User1ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'city', 'state', 'pin_code', 'country']
    list_filter = ['city', 'state', 'pin_code', 'country']


class User2ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone']


class User3ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'ccardnumber']


class User4ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'dcardnumber']


class User5ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'upiid']


class User6ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'paytmnumber']


# admin.site.register(User1Profile, User1ProfileAdmin)
# admin.site.register(User2Profile, User2ProfileAdmin)
# admin.site.register(User3Profile, User3ProfileAdmin)
# admin.site.register(User4Profile, User4ProfileAdmin)
# admin.site.register(User5Profile, User5ProfileAdmin)
# admin.site.register(User6Profile, User6ProfileAdmin)

# admin.site.unregister(User1Profile)
# admin.site.unregister(User2Profile)
# admin.site.unregister(User3Profile)
# admin.site.unregister(User4Profile)
# admin.site.unregister(User5Profile)
# admin.site.unregister(User6Profile)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)