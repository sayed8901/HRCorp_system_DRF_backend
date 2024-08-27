# promotion/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PromotionInfo
from promotion.serializers import PromotionInfoSerializer
from employment.models import EmploymentInfo
from salary.models import SalaryInfo
from job_profile.models import JobProfileHistory
from employee.models import Employee

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly




# Create your views here.
class AllPromotionInfoDetailView(APIView):
    serializer_class = PromotionInfoSerializer
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    # both the standard_user and power_user can GET all the promotion info
    def get(self, request, format = None):
        transfers = PromotionInfo.objects.all()
        serializer = PromotionInfoSerializer(transfers, many=True)

        return Response(serializer.data)
    

    

class PromotionInfoCreateView(generics.CreateAPIView):
    serializer_class = PromotionInfoSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]


    def post(self, request, format=None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found. The provided employee ID may be incorrect.'}, status=status.HTTP_404_NOT_FOUND)


        # Fetch EmploymentInfo and SalaryInfo related to the employee
        try:
            employment_info = EmploymentInfo.objects.get(employee = employee)
            salary_info = SalaryInfo.objects.get(employee = employee)
        except EmploymentInfo.DoesNotExist:
            return Response({'error': 'Employment info not found for this employee.'}, status=status.HTTP_404_NOT_FOUND)
        except SalaryInfo.DoesNotExist:
            return Response({'error': 'Salary info not found for this employee.'}, status=status.HTTP_404_NOT_FOUND)


        # Include the employee ID in the request_data to link it with the transfer record       # Use the employee's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id


        # Initialize the serializer with the data
        serializer = PromotionInfoSerializer(data = request_data)


        if serializer.is_valid():
            # Save the PromotionInfo instance
            promotion_info = serializer.save(employee = employee)


            previous_designation = employment_info.designation
            previous_salary_grade = salary_info.salary_grade
            previous_salary_step = salary_info.salary_step

            new_designation = promotion_info.promoted_to_designation
            new_salary_grade = promotion_info.promoted_salary_grade
            new_salary_step = promotion_info.promoted_salary_step


            # Create a JobProfileHistory entry for "Promotion"
            JobProfileHistory.objects.create(
                employee = promotion_info.employee,
                event_type = 'Promotion',
                event_id = promotion_info.id,

                details = (
                    f'Got Promoted from {previous_designation} (grade {previous_salary_grade} step {previous_salary_step}) to {new_designation} (grade {new_salary_grade} at step {new_salary_step}) with effect from {promotion_info.promotion_effective_date.strftime("%d-%m-%Y")}.'
                ),
                effective_date = promotion_info.promotion_effective_date,
            )


            # Update EmploymentInfo with new promotion details
            employment_info.designation = new_designation

            employment_info.save()

            
            # Also update the salary grade & step in the SalaryInfo model:
            salary_info.salary_grade = new_salary_grade
            salary_info.salary_step = new_salary_step

            salary_info.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

