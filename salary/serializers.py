from rest_framework import serializers
from .models import SalaryInfo

class SalaryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryInfo

        fields = [
            'employee',
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
            'npl_salary_deduction',
            'net_salary',
            'consolidated_salary',
            'is_confirmed',
        ]
        
        # fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
