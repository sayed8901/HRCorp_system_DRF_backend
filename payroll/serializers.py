from rest_framework import serializers
from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    # to get the designation, department & job_location from the model data
    designation = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    job_location = serializers.CharField(read_only=True)

    class Meta:
        model = Payroll

        fields = [
            'employee',
            'month',
            
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
            'festival_bonus',
            'other_allowance',
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

        # fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
        