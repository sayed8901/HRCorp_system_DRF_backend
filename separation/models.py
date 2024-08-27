from django.db import models
from employee.models import Employee
from employee.choices import SEPARATION_CAUSE_CHOICES, CAUSE_WISE_SEPARATION_TYPE_CHOICES


class SeparationInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='employee_id')

    cause_of_separation = models.CharField(max_length=50, choices=SEPARATION_CAUSE_CHOICES)

    application_submission_date = models.DateField()
    separation_effect_date = models.DateField()

    entry_date = models.DateTimeField(auto_now_add=True)


    @property
    def separation_type(self):
         # Convert the list of tuples to a dictionary
        separation_type_dict = dict(CAUSE_WISE_SEPARATION_TYPE_CHOICES)
        return separation_type_dict[self.cause_of_separation]


    def __str__(self):
        return f"{self.employee} - {self.separation_type}"

