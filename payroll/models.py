from django.db import models
from employee.models import Employee
from leave.models import Leave

from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from datetime import datetime
from calendar import monthrange




class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Active')
    month = models.DateField()


    salary_grade = models.PositiveSmallIntegerField()
    salary_step = models.PositiveSmallIntegerField()

    starting_basic = models.DecimalField(max_digits=10, decimal_places=2)
    effective_basic = models.DecimalField(max_digits=10, decimal_places=2)

    house_rent = models.DecimalField(max_digits=10, decimal_places=2)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    conveyance = models.DecimalField(max_digits=10, decimal_places=2)
    hardship = models.DecimalField(max_digits=10, decimal_places=2)
    pf_contribution = models.DecimalField(max_digits=10, decimal_places=2)

    festival_bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)

    pf_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    swf_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    

    npl_salary_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    consolidated_salary = models.DecimalField(max_digits=10, decimal_places=2)

    is_confirmed = models.BooleanField()



    
    class Meta:
        unique_together = ('employee', 'month')
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"

        ordering = ['-month',]




    def calculate_npl_salary_deduction(self):
        """
        This method calculates and stores the NPL salary deduction.
        It is called when processing the payroll.
        """

        # Get the start and end date of the payroll month
        start_of_month = self.month.replace(day=1)
        _, last_day = monthrange(self.month.year, self.month.month)
        end_of_month = self.month.replace(day=last_day)


        # Filter Non_Paid_Leave entries for the current month
        npl_leaves = Leave.objects.filter(
            employee = self.employee,
            leave_type = 'Non_Paid_Leave',
            leave_start_date__lte = end_of_month,
            leave_end_date__gte = start_of_month,
        )


        # Calculate the total number of NPL days in the current month
        total_npl_days = 0

        for leave in npl_leaves:
            leave_start = max(leave.leave_start_date, start_of_month)
            leave_end = min(leave.leave_end_date, end_of_month)

            # Calculate the total number of NPL days
            if leave_start <= leave_end:
                total_npl_days += (leave_end - leave_start).days + 1


        # Calculate and store NPL deduction
        if total_npl_days > 0:
            # Using gross salary for NPL deduction calculation
            npl_salary_deduction = (self.gross_salary / 30) * total_npl_days

            self.npl_salary_deduction = Decimal(npl_salary_deduction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            self.npl_salary_deduction = Decimal('0.00')

        # Save the result to the database
        self.save()




    def calculate_net_salary(self):
        """
        This method calculates and stores the net salary.
        It is called when processing the payroll.
        """
        if self.is_confirmed:
            # Regular net salary for confirmed staff
            result = (
                self.gross_salary -
                (
                    self.pf_deduction +
                    self.swf_deduction +
                    self.tax_deduction +
                    self.npl_salary_deduction
                )
            )
            # for 2 digit decimal precision
            self.net_salary = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            # For non-confirmed staff, net salary is the consolidated salary
            self.net_salary = self.consolidated_salary

        # Save the result to the database
        self.save()




    def __str__(self):
        return f"Payroll for {self.employee} - {self.month.strftime('%Y-%m')}"
