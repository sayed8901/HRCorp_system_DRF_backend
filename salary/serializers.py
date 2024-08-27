from rest_framework import serializers
from .models import SalaryInfo

class SalaryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryInfo
        fields = '__all__'

        read_only_fields = ['employee', ]
