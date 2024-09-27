from django.contrib import admin
from .models import SalaryInfo

# Register your models here.
class SalaryInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = [
        'employee_id', 
        'joining_date',

        'salary_grade', 
        'salary_step', 
        'starting_basic', 
        'effective_basic', 
        'house_rent', 
        'medical_allowance', 
        'conveyance', 
        'hardship', 
        'pf_contribution', 
        'other_allowance', 
        'festival_bonus', 
        'gross_salary', 
        'pf_deduction', 
        'swf_deduction', 
        'tax_deduction', 

        'late_joining_deduction',
        'npl_salary_deduction', 
        'net_salary', 
        # 'consolidated_salary',
        'is_confirmed', 

        'casual_leave_balance', 
        'sick_leave_balance'
    ]

admin.site.register(SalaryInfo, SalaryInfoAdmin)
