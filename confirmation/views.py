# confirmation/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from confirmation.models import ConfirmationInfo
from confirmation.serializers import ConfirmationInfoSerializer
from employment.models import EmploymentInfo 
from salary.models import SalaryInfo 
from job_profile.models import JobProfileHistory
from employee.models import Employee

from datetime import datetime


# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly




# Create your views here.
class AllConfirmationInfoDetailView(APIView):
    serializer_class = ConfirmationInfoSerializer
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    # both the standard_user and power_user can GET all the confirmation info
    def get(self, request, format = None):
        transfers = ConfirmationInfo.objects.all()
        serializer = ConfirmationInfoSerializer(transfers, many=True)

        return Response(serializer.data)





class ConfirmationInfoCreateView(APIView):
    serializer_class = ConfirmationInfoSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]


    def post(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)


         # Fetch EmploymentInfo and SalaryInfo related to the employee
        try:
            employment_info = EmploymentInfo.objects.get(employee = employee)
            salary_info = SalaryInfo.objects.get(employee = employee)
        except EmploymentInfo.DoesNotExist:
            return Response({'error': 'Employment info not found for this employee.'}, status=status.HTTP_404_NOT_FOUND)
        except SalaryInfo.DoesNotExist:
            return Response({'error': 'Salary info not found for this employee.'}, status=status.HTTP_404_NOT_FOUND)


        # Validate if the employee is already confirmed
        if employment_info.is_confirmed:
            return Response({'error': 'The employee has already been confirmed.'}, status=status.HTTP_400_BAD_REQUEST)


        # Validate the confirmation effective date
        confirmation_effective_date_str = request.data.get('confirmation_effective_date')

        if not confirmation_effective_date_str:
            return Response({'error': 'Confirmation effective date is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            confirmation_effective_date = datetime.strptime(confirmation_effective_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format for confirmation effective date. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)


        tentative_date = employment_info.tentative_confirmation_date

        # to validate that the confirmation effective date is on or after the tentative date
        if tentative_date and confirmation_effective_date < tentative_date:
            return Response({'error': 'The confirmation effective date cannot be earlier than the tentative confirmation date.'}, status=status.HTTP_400_BAD_REQUEST)


        # Include the employee ID in the request_data to link it with the transfer record       # Use the employee instance's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id
        

        # Initialize the serializer with the data
        serializer = ConfirmationInfoSerializer(data = request_data)


        if serializer.is_valid():
            # Save the ConfirmationInfo instance
            confirmation_info = serializer.save(employee = employee)


            # Create a JobProfileHistory entry for "Confirmation"
            JobProfileHistory.objects.create(
                employee = confirmation_info.employee,
                event_type = 'Confirmation',
                event_id = confirmation_info.id,

                details=(
                    f'Confirmed as {confirmation_info.confirmed_designation} on grade {confirmation_info.confirmed_grade} at step {confirmation_info.confirmed_step} with effect from {confirmation_info.confirmation_effective_date.strftime("%d-%m-%Y")}.'
                ),
                effective_date = confirmation_info.confirmation_effective_date,
            )


            # Update the EmploymentInfo model:
            # confirmation_effective_date and also to mark the employee as confirmed
            employment_info.confirmation_effective_date = confirmation_info.confirmation_effective_date
            employment_info.is_confirmed = True

            # update the designation too
            employment_info.designation = confirmation_info.confirmed_designation

            employment_info.save()
            


            # Also update the salary grade & step in the SalaryInfo model:
            salary_info.salary_grade = confirmation_info.confirmed_grade
            salary_info.salary_step = confirmation_info.confirmed_step

            salary_info.save()



            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



