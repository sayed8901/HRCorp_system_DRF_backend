from rest_framework import serializers
from .models import PersonalInfo, EmploymentInfo, Department, Designation, JobLocation


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]




class EmploymentInfoSerializer(serializers.ModelSerializer):
    job_location = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=False)
    designation = serializers.StringRelatedField(many=False)

    class Meta:
        model = EmploymentInfo
        fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]




class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'




class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'




class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocation
        fields = '__all__'

