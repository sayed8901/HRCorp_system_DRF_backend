from django.db import models
from employee.models import Employee
from employment.models import Department, JobLocation


class TransferInfo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='employee_id')

    transfer_from_location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True, related_name='transfer_from_location')

    transfer_to_location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True, related_name='transfer_to_location')

    transfer_from_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='transfer_from_department')
    
    transfer_to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='transfer_to_department')
    
    transfer_effective_date = models.DateField()

    entry_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Transfer to {self.transfer_to_location}, with effect from {self.transfer_effective_date.strftime("%d-%m-%Y")} for employee_ID: {self.employee.employee_id}'
    
    