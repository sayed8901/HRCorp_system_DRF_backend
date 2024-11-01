from django.db import models
from employee.models import Employee
from employment.models import Designation
from employee.choices import *



class ConfirmationInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='employee_id')

    confirmed_designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    
    confirmed_grade = models.PositiveSmallIntegerField(choices=SALARY_GRADE_CHOICES)
    confirmed_step = models.PositiveSmallIntegerField(choices=SALARY_STEP_CHOICES)

    confirmation_effective_date = models.DateField()

    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Confirmation Info for {self.employee.employee_id}"
