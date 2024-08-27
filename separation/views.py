from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SeparationInfo
from .serializers import SeparationInfoSerializer
from employee.models import Employee
from employment.models import EmploymentInfo
from job_profile.models import JobProfileHistory

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly




# Create your views here.
class AllSeparationInfoDetailView(APIView):
    serializer_class = SeparationInfoSerializer
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    # both the standard_user and power_user can GET all the separation info
    def get(self, request, format = None):
        transfers = SeparationInfo.objects.all()
        serializer = SeparationInfoSerializer(transfers, many=True)

        return Response(serializer.data)





class SeparationInfoCreateView(generics.CreateAPIView):
    serializer_class = SeparationInfoSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]


    def post(self, request, format=None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch EmploymentInfo and SalaryInfo related to the employee
        try:
            employment_info = EmploymentInfo.objects.get(employee = employee)
        except EmploymentInfo.DoesNotExist:
            return Response({'error': 'Employment info not found for this employee.'}, status=status.HTTP_404_NOT_FOUND)


        # Include the employee ID in the request_data to link it with the transfer record       # Use the employee's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id

        # Initialize the serializer with the data
        serializer = self.get_serializer(data = request_data)


        if serializer.is_valid():
            separation_info = serializer.save(employee = employee)

            # Set the employee status to "Inactive"
            employment_info.status = 'Inactive'
            employment_info.save()


             # Create a JobProfileHistory entry for "Promotion"
            JobProfileHistory.objects.create(
                employee = separation_info.employee,
                event_type = 'Separation',
                event_id = separation_info.id,

                details = (
                    f'{separation_info.separation_type} for "{separation_info.cause_of_separation}" from {employment_info.job_location} with effect from {separation_info.separation_effect_date.strftime("%d-%m-%Y")}.'
                ),
                effective_date = separation_info.separation_effect_date,
            )


            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

