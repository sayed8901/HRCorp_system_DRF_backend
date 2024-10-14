from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payroll
from salary.models import SalaryInfo
from employee.models import Employee
from employment.models import EmploymentInfo
from .serializers import PayrollSerializer

from datetime import datetime


# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly
from power_user.permissions import IsPowerUserOrReadOnly





class PayrollListCreateAPIView(APIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]


    def get(self, request):
        # Retrieve the month query parameter
        month_str = request.query_params.get('month', None)
        
        if not month_str:
            return Response({'detail': 'Month parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert month string to date format (assuming 'YYYY-MM' format)
        try:
            month_date = datetime.strptime(month_str, '%Y-%m').date()
        except ValueError:
            return Response({'detail': 'Invalid month format. Use YYYY-MM.'}, status=status.HTTP_400_BAD_REQUEST)


        # Delete existing payroll records for the requested month
        # This guarantees that each time processing payroll, all employees have their payroll records recreated.
        Payroll.objects.filter(month = month_date).delete()



        # Caching salary info and employment info to minimize database hits
        """
            * Salary info and employment info are cached in dictionaries (salary_info_cache and employment_info_cache). 
            * These caches are keyed by employee.employee_id so that for each employee, the salary and employment information are fetched only once, minimizing database queries during the payroll process.
        """
        _salary_info_cache = {}
        _employment_info_cache = {}



        # Filter active employees based on EmploymentInfo status
        active_employees = Employee.objects.filter(
            employmentinfo__status = 'Active'
        ).select_related('employmentinfo')



        # List to store payroll entries for bulk creation
        payroll_entries = []

        # List to store any errors encountered during processing
        errors = []



        batch_size = 50  # Limit processing to smaller chunks to prevent timeout

        employee_batches = [active_employees[i:i+batch_size] for i in range(0, len(active_employees), batch_size)]


        for employee_batch in employee_batches:
            for employee in employee_batch:
                try:
                    # Cache SalaryInfo to avoid redundant queries
                    if employee.employee_id not in _salary_info_cache:
                        _salary_info_cache[employee.employee_id] = SalaryInfo.objects.get(employee = employee)

                    salary_info = _salary_info_cache[employee.employee_id]


                    # Cache EmploymentInfo to avoid redundant queries
                    if employee.employee_id not in _employment_info_cache:
                        _employment_info_cache[employee.employee_id] = EmploymentInfo.objects.get(employee = employee)

                    employment_info = _employment_info_cache[employee.employee_id]
                    


                    # Creating payroll info for each employee
                    payroll = Payroll(
                        employee = employee,
                        status = employment_info.status, # Active status get from employment_info.status
                        month = month_date,


                        salary_grade = salary_info.salary_grade,
                        salary_step = salary_info.salary_step,

                        starting_basic = salary_info.starting_basic,
                        effective_basic = salary_info.effective_basic,

                        festival_bonus = salary_info.festival_bonus or 0,
                        other_allowance = salary_info.other_allowance or 0,

                        house_rent = salary_info.house_rent,
                        medical_allowance = salary_info.medical_allowance,
                        conveyance = salary_info.conveyance,
                        hardship = salary_info.hardship,
                        pf_contribution = salary_info.pf_contribution,

                        pf_deduction = salary_info.pf_deduction,
                        swf_deduction = salary_info.swf_deduction,
                        tax_deduction = salary_info.tax_deduction,

                        gross_salary = salary_info.gross_salary,


                        consolidated_salary = salary_info.consolidated_salary,
                        is_confirmed = salary_info.is_confirmed,
                    )
                    
                    # Saving the payroll_entries
                    payroll_entries.append(payroll)


                except (SalaryInfo.DoesNotExist, EmploymentInfo.DoesNotExist) as e:
                    errors.append(f"Error for employee {employee.employee_id}: {str(e)}")

            if errors:
                return Response({'errors': errors}, status=status.HTTP_404_NOT_FOUND)
            


            # Bulk insert payroll entries
            """
                * Payroll entries are created in bulk using bulk_create with a batch_size=100, reducing the number of insert operations and improving performance.
            """
            Payroll.objects.bulk_create(payroll_entries, batch_size=100)


            # Calculate NPL salary deduction, late joining deduction, and net salary for each payroll in bulk       # using the methods in the payroll model
            """
                * Batch Payroll Calculation:
                    After all payroll records are inserted, calculations like NPL salary deduction, late joining deduction, and net salary are done in memory, reducing the number of updates to the database.
            """
            for payroll in payroll_entries:
                # Calculating npl salary deduction
                payroll.calculate_npl_salary_deduction()

                # Calculating late joining deduction
                payroll.calculate_late_joining_deduction()

                # Calculating net salary
                payroll.calculate_net_salary()



            # Clear payroll_entries to avoid holding onto data
            payroll_entries.clear()



        # Fetch new payroll records for the specified month
        new_payroll_queryset = Payroll.objects.filter(month = month_date)
        serializer = PayrollSerializer(new_payroll_queryset, many = True)


        return Response(serializer.data)
    




class PayrollRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]

    def get_object(self, pk):
        try:
            return Payroll.objects.get(pk = pk)
        except Payroll.DoesNotExist:
            return None



    def get(self, request, pk):
        payroll = self.get_object(pk)

        if payroll is not None:
            serializer = PayrollSerializer(payroll)
            return Response(serializer.data)
        
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)



    def put(self, request, pk):
        payroll = self.get_object(pk)

        if payroll is not None:
            serializer = PayrollSerializer(payroll, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)



    def delete(self, request, pk):
        payroll = self.get_object(pk)

        if payroll is not None:
            payroll.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    

