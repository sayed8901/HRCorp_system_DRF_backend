from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from employee.models import Employee
from salary.models import SalaryInfo
from .models import Leave
from .serializers import LeaveSerializer

from datetime import datetime


# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly
from power_user.permissions import IsPowerUserOrReadOnly





# Utility function to update leave balances
def update_leave_balances(employee, days_taken, leave_type, increase=False):
    try:
        salary_info = SalaryInfo.objects.get(employee=employee)


        if leave_type == 'Casual':
            # Check if there are enough casual leave days available
            if not increase and salary_info.casual_leave_balance < days_taken:
                raise ValueError("Insufficient casual leave balance")
            
            else:
                if increase:
                    salary_info.casual_leave_balance += days_taken
                else:
                    salary_info.casual_leave_balance -= days_taken


        elif leave_type == 'Sick':
            # Check if there are enough sick leave days available
            if not increase and salary_info.sick_leave_balance < days_taken:
                raise ValueError("Insufficient sick leave balance")
            
            else:
                if increase:
                    salary_info.sick_leave_balance += days_taken
                else:
                    salary_info.sick_leave_balance -= days_taken


        salary_info.save()


    except SalaryInfo.DoesNotExist:
        raise ValueError("Salary info not found for the employee")





# Create your views here.
class AllLeaveInfoDetailView(APIView):
    serializer_class = LeaveSerializer
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]

    def get(self, request, format=None):
        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)

        return Response(serializer.data)





# both the standard_user and power_user can GET or POST a leave info
class IndividualEmployeeLeaveInfoView(APIView):
    serializer_class = LeaveSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]



    # To get all leave information of an employee
    def get(self, request, format=None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
            # print(employee)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)

        leaves = Leave.objects.filter(employee = employee_id)

        serializer = LeaveSerializer(leaves, many=True)
        # print('leave info:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)





    # To post leave information
    def post(self, request, format=None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)


        # Include the employee ID in the request_data to link it with the leave record       # Use the employee instance's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id


        # Calculate days_taken from leave_start_date and leave_end_date
        leave_start_date = request_data.get('leave_start_date')
        leave_end_date = request_data.get('leave_end_date')

        if not leave_start_date or not leave_end_date:
            return Response({'error': 'leave_start_date and leave_end_date are required'}, status=status.HTTP_400_BAD_REQUEST)


        # Calculate the number of days
        leave_duration = (datetime.strptime(leave_end_date, '%Y-%m-%d') - datetime.strptime(leave_start_date, '%Y-%m-%d')).days + 1

        # Ensure that leave duration is a positive number
        if leave_duration <= 0:
            return Response({'error': 'Invalid leave duration, end date must be after start date'}, status=status.HTTP_400_BAD_REQUEST)


        # Check the leave balance before saving the leave record
        leave_type = request_data['leave_type']

        # Deduct the leave days after saving the leave record
        try:
            update_leave_balances(employee, leave_duration, leave_type, increase=False)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        # Save the leave record
        serializer = LeaveSerializer(data = request_data)

        if serializer.is_valid():
            # If balance is sufficient, save the leave record
            serializer.save(employee = employee)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# To update leave information by power_user only
class UpdateSingleLeaveInfoView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]


    # To update leave information
    def put(self, request, format=None):
        leave_id = request.query_params.get('leave_id')

        if not leave_id:
            return Response({'error': 'leave_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the specific leave record using transfer_id
            leave = Leave.objects.get(id = leave_id)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave info not found, may be incorrect leave ID given'}, status=status.HTTP_404_NOT_FOUND)


        # Store the original leave days for balance adjustment
        original_days_taken = leave.days_taken


        serializer = LeaveSerializer(leave, data = request.data, partial=True)


        if serializer.is_valid():
            # Calculate the difference in days
            new_days_taken = request.data.get('days_taken', leave.days_taken)
            days_difference = int(new_days_taken) - original_days_taken


            # If days have increased, check if there is enough leave balance
            if days_difference > 0:
                try:
                    update_leave_balances(leave.employee, days_difference, leave.leave_type, increase=False)
                except ValueError as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


            # Save the updated leave record
            leave = serializer.save()


            # Adjust the leave balance based on the difference in days
            if days_difference != 0:
                update_leave_balances(
                    leave.employee, 
                    abs(days_difference), 
                    leave.leave_type, 
                    increase=(days_difference < 0)
                )

            return Response(serializer.data, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# To delete the last leave information by power_user only
class WithdrawSingleLeaveInfoView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]

    # To delete leave information
    def delete(self, request, format=None):
        leave_id = request.query_params.get('leave_id')

        if not leave_id:
            return Response({'error': 'leave_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the specific leave record using transfer_id
            leave = Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave info not found, may be incorrect leave ID given'}, status=status.HTTP_404_NOT_FOUND)
        

        # Save the leave days before deleting
        days_taken = leave.days_taken
        leave_type = leave.leave_type
        employee = leave.employee


        leave.delete()


        # Restore the leave days after deleting the leave record
        try:
            update_leave_balances(employee, days_taken, leave_type, increase=True)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
        return Response({'message': 'Leave information deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


