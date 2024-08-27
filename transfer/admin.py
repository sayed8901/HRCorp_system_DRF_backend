from django.contrib import admin
from .models import TransferInfo

# Register your models here.
class TransferInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['id', 'employee_id', 'transfer_from_location', 'transfer_to_location', 'transfer_from_department', 'transfer_to_department', 'transfer_effective_date', 'entry_date']

admin.site.register(TransferInfo, TransferInfoAdmin)
