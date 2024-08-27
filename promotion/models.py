from django.db import models
from employee.models import Employee
from employment.models import Designation
from employee.choices import *


class PromotionInfo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='employee_id')

    promoted_to_designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, related_name='promotions_to')
    
    promoted_salary_grade = models.PositiveSmallIntegerField(choices=SALARY_GRADE_CHOICES)
    promoted_salary_step = models.PositiveSmallIntegerField(choices=SALARY_STEP_CHOICES)

    promotion_effective_date = models.DateField()

    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Promotion Info for {self.employee.employee_id}"
