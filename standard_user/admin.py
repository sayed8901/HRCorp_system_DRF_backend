from django.contrib import admin
from .models import StandardUser


# Register your models here.
class StandardUserAdmin(admin.ModelAdmin):
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
    
    def supervisor(self, obj):
        return obj.supervisor.username
    
    list_display = ['id', 'user', 'first_name', 'last_name', 'contact_no', 'email', 'user_type', 'supervisor']


admin.site.register(StandardUser, StandardUserAdmin)

