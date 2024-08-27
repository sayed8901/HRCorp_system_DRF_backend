from django.contrib import admin
from .models import PersonalInfo, EmploymentInfo, Department, Designation, JobLocation


# Register your models here.
class PersonalInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'name', 'gender', 'father_name', 'mother_name', 'marital_status', 'spouse_name', 'permanent_address', 'present_address', 'date_of_birth', 'smart_id', 'contact_number', 'email', 'educational_degree', 'blood_group',]

admin.site.register(PersonalInfo, PersonalInfoAdmin)



class EmploymentInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'status', 'designation', 'department', 'job_location', 'joining_date', 'probation_period_months', 'tentative_confirmation_date', 'is_confirmed', 'confirmation_effective_date']

admin.site.register(EmploymentInfo, EmploymentInfoAdmin)



class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug']

admin.site.register(Department, DepartmentAdmin)



class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug']

admin.site.register(Designation, DesignationAdmin)



class JobLocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug']

admin.site.register(JobLocation, JobLocationAdmin)



