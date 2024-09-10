from django.db import models
from employee.models import Employee

from employee.choices import LEAVE_TYPE_CHOICES



class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='employee_id')

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)

    leave_start_date = models.DateField()
    leave_end_date = models.DateField()

    entry_date = models.DateTimeField(auto_now_add=True)


    @property
    def days_taken(self):
        if self.leave_start_date and self.leave_end_date:
            # Calculate the number of days including both start and end date
            return (self.leave_end_date - self.leave_start_date).days + 1
        
        return 0
        
    


    def __str__(self):
        return f"{self.employee} - {self.leave_type} leave taken from {self.leave_start_date} to {self.leave_end_date}"

