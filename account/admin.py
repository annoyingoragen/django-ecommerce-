from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=['username','email','first_name','last_name','phone_number','is_active','date_joined']
    filter_horizontal=()
    readonly_fields=('date_joined','last_login')
    list_filter=()
    fieldsets=()
    ordering=('-date_joined',)

admin.site.register(Account,AccountAdmin)