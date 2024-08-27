from rest_framework import serializers
from .models import Employee
from employment.models import PersonalInfo, EmploymentInfo
from salary.models import SalaryInfo
from job_profile.models import JobProfileHistory



class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

        read_only_fields = ['employee']



class EmploymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentInfo
        fields = '__all__'

        read_only_fields = ['employee']



class SalaryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryInfo
        fields = '__all__'

        read_only_fields = ['employee']





class EmployeeSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer(read_only=True)
    # Add write-only field for handling the creation & updating purpose
    personal_info_data = PersonalInfoSerializer(write_only=True)

    employment_info = EmploymentInfoSerializer(read_only=True)
    # Add write-only field for handling the creation & updating purpose
    employment_info_data = EmploymentInfoSerializer(write_only=True)

    salary_info = SalaryInfoSerializer(read_only=True)
    # Add write-only field for handling the creation & updating purpose
    salary_info_data = SalaryInfoSerializer(write_only=True)

    class Meta:
        model = Employee
        fields = '__all__'



    def create(self, validated_data):
        # Extract the write-only fields from validated_data
        personal_info_data = validated_data.pop('personal_info_data', None)
        employment_info_data = validated_data.pop('employment_info_data', None)
        salary_info_data = validated_data.pop('salary_info_data', None)

        # Create the Employee instance
        employee = Employee.objects.create(**validated_data)

        if personal_info_data:
            # Create PersonalInfo instance linked to the newly created Employee
            personal_info = PersonalInfo.objects.create(employee = employee, **personal_info_data)
            
        if employment_info_data:
            # Create EmploymentInfo instance linked to the newly created Employee
            employment_info = EmploymentInfo.objects.create(employee = employee, **employment_info_data)

        if salary_info_data:
            # Create SalaryInfo instance linked to the newly created Employee
            SalaryInfo.objects.create(employee = employee, **salary_info_data)
        

        # Create JobProfileHistory entry for "New Joining"
        JobProfileHistory.objects.create(
            employee = employee,
            event_type = 'Joining',
            
            details = (
                f'{personal_info.name} has joined as {employment_info.designation} at {employment_info.job_location} in the {employment_info.department} department on {employment_info.joining_date.strftime("%d-%m-%Y")}.'
            ),
            effective_date = employment_info.joining_date
        )


        return employee



    def update(self, instance, validated_data):
        # Extract the write-only fields from validated_data
        personal_info_data = validated_data.pop('personal_info_data', None)
        employment_info_data = validated_data.pop('employment_info_data', None)
        salary_info_data = validated_data.pop('salary_info_data', None)

        # Update the Employee instance
        instance = super().update(instance, validated_data)

        if personal_info_data:
            # Update or create PersonalInfo instance linked to the Employee
            personal_info, created = PersonalInfo.objects.get_or_create(employee = instance)
            
            # Update the fields of PersonalInfo
            for attr, value in personal_info_data.items():
                setattr(personal_info, attr, value)

            personal_info.save()


        if employment_info_data:
            # Update or create EmploymentInfo instance linked to the Employee
            employment_info, created = EmploymentInfo.objects.get_or_create(employee = instance)
            
            # Update the fields of PersonalInfo
            for attr, value in employment_info_data.items():
                setattr(employment_info, attr, value)

            employment_info.save()


        if salary_info_data:
            # Update or create SalaryInfo instance linked to the Employee
            salary_info, created = SalaryInfo.objects.get_or_create(employee = instance)
            
            # Update the fields of PersonalInfo
            for attr, value in salary_info_data.items():
                setattr(salary_info, attr, value)

            salary_info.save()


        return instance
    

