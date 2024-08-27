from django.contrib import admin
from .models import SeparationInfo


# Register your models here.
class SeparationInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee', 'separation_type', 'cause_of_separation', 'application_submission_date', 'separation_effect_date', 'entry_date']

admin.site.register(SeparationInfo, SeparationInfoAdmin)
