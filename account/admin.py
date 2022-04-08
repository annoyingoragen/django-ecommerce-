from django.contrib import admin
from .models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="70" style="border-radius:50%;">'.format(object.profile_picture.url))

    thumbnail.short_description='Profile Picture'
    list_display=['thumbnail','user','city','state','country']

class AccountAdmin(UserAdmin):
    list_display=['username','email','first_name','last_name','phone_number','is_active','date_joined']
    filter_horizontal=()
    readonly_fields=('date_joined','last_login')
    list_filter=()
    fieldsets=()
    ordering=('-date_joined',)

admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)