from django.contrib import admin
from .models import Payroll

# Register your models here.
class PayrollAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = [
        'id',
        'month', 
        'employee_id', 

        'employee_name',
        'joining_date',
        'designation',
        'department',
        'job_location',
        'status', 

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
        'consolidated_salary',
        'is_confirmed', 
    ]

admin.site.register(Payroll, PayrollAdmin)
