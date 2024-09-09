from django.contrib import admin
from .models import Payroll

# Register your models here.
class PayrollAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'month', 'status', 'is_confirmed', 'salary_grade', 'salary_step', 'starting_basic', 'salary_step', 'effective_basic', 'other_allowance', 'festival_bonus', 'house_rent', 'medical_allowance', 'conveyance', 'hardship', 'pf_contribution', 'gross_salary', 'pf_deduction', 'swf_deduction', 'npl_deduction', 'tax_deduction', 'net_salary', 'consolidated_salary']

admin.site.register(Payroll, PayrollAdmin)
