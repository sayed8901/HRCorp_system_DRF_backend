from django.db import models
from employee.models import Employee
from leave.models import Leave
from employment.models import EmploymentInfo  
from employee.choices import *

from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP




class SalaryInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='employee_id')

    salary_grade = models.PositiveSmallIntegerField(choices=SALARY_GRADE_CHOICES)
    salary_step = models.PositiveSmallIntegerField(choices=SALARY_STEP_CHOICES)

    starting_basic = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    effective_basic = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    festival_bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    casual_leave_balance = models.PositiveIntegerField(default=10)
    sick_leave_balance = models.PositiveIntegerField(default=14)

    npl_salary_deduction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)



    # to calculate the starting basic based on the selected grade
    # also to calculate the effective basic based on the selected salary_step
    def clean(self):
        grade_dict = dict(GRADE_WISE_STARTING_BASIC_SALARY_CHOICES)
        if self.salary_grade not in grade_dict:
            raise ValidationError("Invalid salary grade.")

        # Set the starting_basic salary based on the grade
        self.starting_basic = Decimal(grade_dict[self.salary_grade])

        # Calculate effective_basic based on salary_step 
        # Assume each salary_step increases the basic by 10%
        self.effective_basic = (self.starting_basic + (self.starting_basic * Decimal('0.10')) * Decimal(self.salary_step)) - (self.starting_basic * Decimal('0.10'))



    # to check if the staff is confirmed or not
    @property
    def is_confirmed(self):
        try:
            employment_info = EmploymentInfo.objects.get(employee = self.employee)
            return employment_info.is_confirmed
        except EmploymentInfo.DoesNotExist:
            return False


    # house rent (50% of effective basic)
    @property
    def house_rent(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.50')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')


    # medical allowance (20% of effective basic)
    @property
    def medical_allowance(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.20')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')
        

    # conveyance allowance (10% of effective basic)
    @property
    def conveyance(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.10')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')
    

    # hardship allowance (10% of effective basic)
    @property
    def hardship(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.10')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')


    # PF contribution (10% of effective basic)
    @property
    def pf_contribution(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.10')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')


    # PF deduction (20% of effective basic)
    @property
    def pf_deduction(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.20')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')


    # SWF deduction (1% of effective basic)
    @property
    def swf_deduction(self):
        if self.is_confirmed: 
            result = self.effective_basic * Decimal('0.01')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')
    

    @property
    def tax_deduction(self):
        # Tax deduction if effective basic salary is >= 20000
        if self.is_confirmed and self.effective_basic >= 20000:
            return Decimal('500.00')    # tk 500.00 tax deduction
        return Decimal('0.00')
    


    @property
    def gross_salary(self):
        if self.is_confirmed:
            # Regular gross salary for confirmed staff
            result = (
                self.effective_basic +
                self.house_rent +
                self.medical_allowance +
                self.conveyance +
                self.hardship +
                self.pf_contribution +
                (self.other_allowance or Decimal('0.00')) +
                (self.festival_bonus or Decimal('0.00'))
            )
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            # For non-confirmed staff, gross salary is the consolidated salary
            return self.consolidated_salary


    # method to update the leave balance status
    def update_leave_balances(self):
        # Fetch leave records and update balances accordingly
        leave_records = Leave.objects.filter(employee=self.employee, status='Approved')

        for record in leave_records:
            if record.leave_type == 'Casual':
                self.casual_leave_balance -= record.days_taken
            elif record.leave_type == 'Sick':
                self.sick_leave_balance -= record.days_taken


    def calculate_npl_deduction(self):
        if self.casual_leave_balance < 0:
            npl_days = abs(self.casual_leave_balance)
            npl_deduction = (self.effective_basic / 30) * npl_days  # Assuming 30 days in a month
            return Decimal(npl_deduction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')



    @property
    def net_salary(self):
        npl_salary_deduction = self.calculate_npl_deduction()

        if self.is_confirmed:
            # Regular net salary for confirmed staff
            result = (
                self.gross_salary -
                (
                    self.pf_deduction +
                    self.swf_deduction +
                    (self.npl_salary_deduction or Decimal('0.00')) +
                    self.tax_deduction
                    + npl_salary_deduction
                )
            )
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            # For non-confirmed staff, net salary is the consolidated salary
            return self.consolidated_salary
        


    # Consolidated salary (150% of effective basic)
    @property
    def consolidated_salary(self):
        if not self.is_confirmed: 
            # Consolidated salary is 150% of the effective basic salary
            result = self.effective_basic * Decimal('1.5')
            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')




    def save(self, *args, **kwargs):
        # Call the clean method to calculate the starting_basic and effective_basic
        self.clean()

        super().save(*args, **kwargs)





    def __str__(self):
        try:
            if self.is_confirmed:
                return f"{self.employee.employee_id} - Gross: {self.gross_salary}, Net: {self.net_salary}"
            else:
                return f"{self.employee.employee_id} - Consolidated: {self.consolidated_salary}"
            
        except EmploymentInfo.DoesNotExist:
            return f"{self.employee.employee_id} - No Employment Info"




