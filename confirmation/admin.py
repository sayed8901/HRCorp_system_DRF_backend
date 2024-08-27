from django.contrib import admin
from .models import ConfirmationInfo


# Register your models here.
class ConfirmationInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'confirmed_designation', 'confirmed_grade', 'confirmed_step', 'confirmation_effective_date', 'entry_date']

admin.site.register(ConfirmationInfo, ConfirmationInfoAdmin)