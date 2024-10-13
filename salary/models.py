from django.db import models
from employee.models import Employee
from leave.models import Leave
from employment.models import EmploymentInfo

from employee.choices import *

from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange





class SalaryInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete = models.CASCADE, to_field = 'employee_id')

    salary_grade = models.PositiveSmallIntegerField(choices = SALARY_GRADE_CHOICES)
    salary_step = models.PositiveSmallIntegerField(choices = SALARY_STEP_CHOICES)

    starting_basic = models.DecimalField(max_digits = 10, decimal_places = 2, editable = False)
    effective_basic = models.DecimalField(max_digits = 10, decimal_places = 2, editable = False)

    festival_bonus = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    other_allowance = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)


    casual_leave_balance = models.PositiveIntegerField(default = 10)
    sick_leave_balance = models.PositiveIntegerField(default = 14)





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
        self.effective_basic = (self.starting_basic + 
                                    (self.starting_basic * Decimal('0.10')) * Decimal(self.salary_step)
                               ) - (self.starting_basic * Decimal('0.10'))




    # Retrieve the EmploymentInfo for the employee.
    # to find the confirmation status & joining date later on..
    def get_employment_info(self):
        try:
            return EmploymentInfo.objects.select_related('employee').get(employee = self.employee)
        except EmploymentInfo.DoesNotExist:
            return None



    @property
    def joining_date(self):
        try:
            employment_info = self.get_employment_info()
            return employment_info.joining_date
        except EmploymentInfo.DoesNotExist:
            return None
    


    # to check if the staff is confirmed or not
    @property
    def is_confirmed(self):
        try:
            employment_info = self.get_employment_info()
            return employment_info.is_confirmed
        except EmploymentInfo.DoesNotExist:
            return False





    # creating common function to calculate allowance amount for different fields
    def calculate_allowance_amount(self, percentage):
        if self.is_confirmed:
            result = self.effective_basic * Decimal(percentage)

            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return Decimal('0.00')
    
    

    # Define various allowances as properties

    # house rent (50% of effective basic)
    @property
    def house_rent(self):
        return self.calculate_allowance_amount('0.50')


    # medical allowance (20% of effective basic)
    @property
    def medical_allowance(self):
        return self.calculate_allowance_amount('0.20')
        

    # conveyance allowance (10% of effective basic)
    @property
    def conveyance(self):
        return self.calculate_allowance_amount('0.10')
    

    # hardship allowance (10% of effective basic)
    @property
    def hardship(self):
        return self.calculate_allowance_amount('0.10')


    # PF contribution (10% of effective basic)
    @property
    def pf_contribution(self):
        return self.calculate_allowance_amount('0.10')


    # PF deduction (20% of effective basic)
    @property
    def pf_deduction(self):
        return self.calculate_allowance_amount('0.20')


    # SWF deduction (1% of effective basic)
    @property
    def swf_deduction(self):
        return self.calculate_allowance_amount('0.01')
    


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





    # Consolidated salary (150% of effective basic)
    @property
    def consolidated_salary(self):
        if not self.is_confirmed: 
            # Consolidated salary is 150% of the effective basic salary
            result = self.effective_basic * Decimal('1.5')

            # for 2 digit decimal precision
            return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return Decimal('0.00')
    

    
    # # In this case, the setter doesn’t have to do anything special because i'm calculating consolidated_salary within the property itself. 
    # # However, this setter allows the consolidated_salary to be "set" without raising the error.
    
    # @consolidated_salary.setter
    # def consolidated_salary(self, value):
    #     pass





    @property
    def late_joining_deduction(self):
        joining_date = self.joining_date

        # Get the current date
        now = timezone.now().date()  # Convert to date
        start_of_month = now.replace(day=1)

        # Calculate the end of the current month
        _, last_day_of_month = monthrange(now.year, now.month)
        end_of_month = now.replace(day=last_day_of_month)

        # Deduct salary based on joining date
        days_in_month = last_day_of_month

        if joining_date and joining_date > end_of_month:
            return Decimal('0.00')  # Joined after the current month

        # Determine the deduction based on joining date
        if joining_date and joining_date < start_of_month:
            deduction_days = 0  # No deduction if joined before the month starts
        elif joining_date and joining_date >= start_of_month:
            days_worked = (end_of_month - joining_date).days + 1
            deduction_days = days_in_month - days_worked
        else:
            deduction_days = days_in_month

        # Calculate the deduction amount
        if self.is_confirmed:
            deduction = (self.gross_salary / days_in_month) * deduction_days
        else:
            deduction = (self.consolidated_salary / days_in_month) * deduction_days

        return deduction.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)





    @property
    def npl_salary_deduction(self):
        now = timezone.now()

        # Get the start and end date of the current month
        start_of_month = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
        end_of_month = (start_of_month + timezone.timedelta(days = 31)).replace(day = 1) - timezone.timedelta(seconds=1)


        # Filter Non_Paid_Leave entries for the current month
        npl_leaves = Leave.objects.select_related('employee').filter(
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
            # Choose salary type for deduction
            if self.is_confirmed:
                salary_for_deduction = self.gross_salary
            else:
                salary_for_deduction = self.consolidated_salary

            # Using gross salary for NPL deduction calculation
            npl_salary_deduction = (salary_for_deduction / 30) * total_npl_days
            print('check npl_salary_deduction:', 'total_npl_days', total_npl_days, ', npl_salary_deduction', npl_salary_deduction)

            return Decimal(npl_salary_deduction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            return Decimal('0.00')





    @property
    def net_salary(self):
        if self.is_confirmed:
            # Regular net salary for confirmed staff
            deductions = (
                self.pf_deduction +
                self.swf_deduction +
                self.tax_deduction +
                self.npl_salary_deduction + 
                self.late_joining_deduction
            )
            net_salary_amount = self.gross_salary - deductions

            # for 2 digit decimal precision
            return net_salary_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        else:
            # For non-confirmed staff, adjust the consolidated salary
            if self.consolidated_salary > 0:
                # Deduct NPL salary deduction from consolidated salary
                net_salary = self.consolidated_salary - (
                    self.npl_salary_deduction + 
                    self.late_joining_deduction
                )

            else:
                # If no consolidated salary is set, default net salary to 0
                net_salary = Decimal('0.00')
            
            # Round to 2 decimal places
            return net_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            




    def save(self, *args, **kwargs):
        # Call the clean method to calculate the starting_basic and effective_basic
        self.clean()

        # # Update consolidated_salary with net_salary for non-confirmed staff
        # if not self.is_confirmed:
        #     self.consolidated_salary = self.net_salary

        super().save(*args, **kwargs)





    def __str__(self):
        try:
            if self.is_confirmed:
                return f"{self.employee.employee_id} - Gross: {self.gross_salary}, Net: {self.net_salary}"
            else:
                return f"{self.employee.employee_id} - Consolidated: {self.consolidated_salary}"
            
        except EmploymentInfo.DoesNotExist:
            return f"{self.employee.employee_id} - No Employment Info"
