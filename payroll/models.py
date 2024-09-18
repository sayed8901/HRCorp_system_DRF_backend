from django.db import models
from employee.models import Employee
from employment.models import EmploymentInfo
from employment.models import PersonalInfo
from leave.models import Leave

from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange




class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Inactive')
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
    late_joining_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    consolidated_salary = models.DecimalField(max_digits=10, decimal_places=2)

    is_confirmed = models.BooleanField()



    
    class Meta:
        unique_together = ('employee', 'month')
        verbose_name = "Payroll"
        verbose_name_plural = "Payrolls"
        
        ordering = ['-month',]  # sorting by month



    # Retrieve the PersonalInfo for the employee.
    def get_personal_info(self):
        try:
            return PersonalInfo.objects.get(employee = self.employee)
        except PersonalInfo.DoesNotExist:
            return None

    # Retrieve the EmploymentInfo for the employee.
    def get_employment_info(self):
        try:
            return EmploymentInfo.objects.get(employee = self.employee)
        except EmploymentInfo.DoesNotExist:
            return None
        

    @property
    def employee_name(self):
        personal_info = self.get_personal_info()
        if personal_info:
            return personal_info.name
        return 'N/A'

    @property
    def designation(self):
        employment_info = self.get_employment_info()
        if employment_info:
            return employment_info.designation
        return 'N/A'

    @property
    def department(self):
        employment_info = self.get_employment_info()
        if employment_info:
            return employment_info.department
        return 'N/A'

    @property
    def job_location(self):
        employment_info = self.get_employment_info()
        if employment_info:
            return employment_info.job_location
        return 'N/A'

    @property
    def joining_date(self):
        employment_info = self.get_employment_info()
        if employment_info:
            return employment_info.joining_date
        return None



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
            # Choose salary type for deduction
            if self.is_confirmed:
                salary_for_deduction = self.gross_salary
            else:
                salary_for_deduction = self.consolidated_salary

            # Using gross salary for NPL deduction calculation
            npl_salary_deduction = (salary_for_deduction / 30) * total_npl_days
            print('check npl_salary_deduction:', 'total_npl_days', total_npl_days, ', npl_salary_deduction', npl_salary_deduction)

            self.npl_salary_deduction = Decimal(npl_salary_deduction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            self.npl_salary_deduction = Decimal('0.00')
        

        # Deduct salary based on joining date
        joining_date = self.joining_date

        if joining_date and joining_date.month == self.month.month and joining_date.year == self.month.year:
            days_in_month = (end_of_month - start_of_month).days + 1
            
            days_worked = (end_of_month - joining_date).days + 1
            deduction_days = days_in_month - days_worked
            print("deduction_days:", deduction_days)

            if self.is_confirmed:
                self.gross_salary -= (self.gross_salary / days_in_month) * deduction_days
            else:
                self.consolidated_salary -= (self.consolidated_salary / days_in_month) * deduction_days


            # **Calculate late joining deduction**
            if self.is_confirmed:
                self.late_joining_deduction = (self.gross_salary / days_in_month) * deduction_days
            else:
                self.late_joining_deduction = (self.consolidated_salary / days_in_month) * deduction_days
            

            

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
            # For non-confirmed staff, adjust the consolidated salary
            if self.consolidated_salary > 0:
                # Deduct NPL salary deduction from consolidated salary
                self.net_salary = self.consolidated_salary - self.npl_salary_deduction
            else:
                # If no consolidated salary is set, default net salary to 0
                self.net_salary = Decimal('0.00')
            
            # Round to 2 decimal places
            self.net_salary = self.net_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Save the result to the database
        self.save()




    def __str__(self):
        return f"Payroll for {self.employee} - {self.month.strftime('%Y-%m')}"

