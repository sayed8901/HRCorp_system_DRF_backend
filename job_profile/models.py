from django.db import models
from employee.models import Employee

from employee.choices import EVENT_TYPE_CHOICES


class JobProfileHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='employee_id')

    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_id = models.CharField(max_length=10, blank=True, null=True, help_text="ID of the event related to this job profile history")

    details = models.TextField()
    effective_date = models.DateField()


    def __str__(self):
        return f'Profile_status: {self.event_type} on: {self.effective_date.strftime("%d-%m-%Y")} for employee_ID: {self.employee.employee_id}'

