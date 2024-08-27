from django.contrib import admin
from .models import JobProfileHistory

# Register your models here.
class JobProfileHistoryAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['id', 'employee_id', 'event_type', 'event_id', 'details', 'effective_date', ]

admin.site.register(JobProfileHistory, JobProfileHistoryAdmin)