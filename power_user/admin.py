from django.contrib import admin
from .models import PowerUser

# Register your models here.
class PowerUserAdmin(admin.ModelAdmin):
    def user(self, obj):
        return obj.user.username
    
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def email(self, obj):
        return obj.user.email
    
    def user_type(self, obj):
        return obj.user.user_type
    
    list_display = ['id', 'user', 'first_name', 'last_name', 'contact_no', 'email', 'user_type']

admin.site.register(PowerUser, PowerUserAdmin)
