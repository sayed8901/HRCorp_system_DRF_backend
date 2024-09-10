from django.db import models
from employee.models import Employee
from leave.models import Leave

from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from datetime import datetime





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





    @property
    def npl_salary_deduction(self):
        now = timezone.now()

        # Get the start and end date of the current month
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(seconds=1)


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
            # Ensure leave_start_date and leave_end_date are datetime objects
            if not isinstance(leave.leave_start_date, datetime):
                leave.leave_start_date = timezone.make_aware(datetime.combine(leave.leave_start_date, datetime.min.time()))
                
            if not isinstance(leave.leave_end_date, datetime):
                leave.leave_end_date = timezone.make_aware(datetime.combine(leave.leave_end_date, datetime.min.time()))


            leave_start = max(leave.leave_start_date, start_of_month)
            leave_end = min(leave.leave_end_date, end_of_month)

            # Calculate the total number of NPL days
            if leave_start <= leave_end:
                total_npl_days += (leave_end - leave_start).days + 1


        # Calculate the deduction
        if total_npl_days > 0:
            npl_deduction = (self.effective_basic / 30) * total_npl_days  # Assuming 30 days in a month

            return Decimal(npl_deduction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        

        return Decimal('0.00')





    @property
    def net_salary(self):
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
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            # For non-confirmed staff, net salary is the consolidated salary
            return self.consolidated_salary





    def __str__(self):
        return f"{self.employee} - {self.month.strftime('%Y-%m')}"

