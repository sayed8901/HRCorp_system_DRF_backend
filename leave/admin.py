from django.contrib import admin
from .models import Leave

# Register your models here.
class LeaveAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'leave_type', 'leave_start_date', 'leave_end_date', 'days_taken' ]

admin.site.register(Leave, LeaveAdmin)
