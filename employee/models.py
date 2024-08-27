from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, primary_key=True, editable=False)
    # editable=False: This prevents users from manually editing the employee_id in the Django Admin panel or forms.

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by('-employee_id').first()

            if last_employee:
                last_id = int(last_employee.employee_id)
                # Generate the next employee_id in the format '0001', '0002', etc.
                next_new_id = f"{last_id + 1:04}"
            else:
                next_new_id = "0001"

            self.employee_id = next_new_id

        super().save(*args, **kwargs)


    def __str__(self):
        return self.employee_id
