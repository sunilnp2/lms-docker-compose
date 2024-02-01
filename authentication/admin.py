from django.contrib import admin
from authentication.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'membership_date']
    list_display_links = ['id', 'name', 'email', 'membership_date']
admin.site.register(User,UserAdmin)
