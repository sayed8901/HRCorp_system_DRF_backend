from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payroll
from salary.models import SalaryInfo
from leave.models import Leave
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
        


        # Check if payroll already exists for the requested month
        existing_payroll = Payroll.objects.filter(month=month_date)
        
        if existing_payroll.exists():
            serializer = PayrollSerializer(existing_payroll, many=True)
            return Response(serializer.data)
        


        # Generate payroll if it does not exist

        # Filter active employees based on EmploymentInfo status
        active_employees = Employee.objects.filter(
            employmentinfo__status = 'Active'
        ).select_related('employmentinfo')


        for employee in active_employees:
            try:
                salary_info = SalaryInfo.objects.get(employee = employee)
                leave_info = Leave.objects.filter(employee = employee)

                employment_info = EmploymentInfo.objects.get(employee = employee)
                

                # updating leave balance status
                leave_info.update_leave_balances()
                

                # Creating payroll info for each employee
                Payroll.objects.create(
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

                    npl_salary_deduction = salary_info.npl_salary_deduction, # Deduct NPL salary

                    net_salary = salary_info.net_salary,

                    consolidated_salary = salary_info.consolidated_salary,
                    is_confirmed = salary_info.is_confirmed,
                )

            except (SalaryInfo.DoesNotExist, EmploymentInfo.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

                    
        # Query payroll records for the specified month
        new_payroll_queryset = Payroll.objects.filter(month = month_date)
        serializer = PayrollSerializer(new_payroll_queryset, many=True)

        return Response(serializer.data)






class PayrollRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]

    def get_object(self, pk):
        try:
            return Payroll.objects.get(pk=pk)
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
    

