from django.db import models
from employee.models import Employee


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()


    salary_grade = models.PositiveSmallIntegerField()
    salary_step = models.PositiveSmallIntegerField()

    starting_basic = models.DecimalField(max_digits=10, decimal_places=2)
    effective_basic = models.DecimalField(max_digits=10, decimal_places=2)

    festival_bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    house_rent = models.DecimalField(max_digits=10, decimal_places=2)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance = models.DecimalField(max_digits=10, decimal_places=2)
    hardship = models.DecimalField(max_digits=10, decimal_places=2)
    pf_contribution = models.DecimalField(max_digits=10, decimal_places=2)

    pf_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    swf_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    
    consolidated_salary = models.DecimalField(max_digits=10, decimal_places=2)

    is_confirmed = models.BooleanField()
    
    status = models.CharField(max_length=10, default='Active')


    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    npl_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    def __str__(self):
        return f"{self.employee} - {self.month.strftime('%Y-%m')}"

