from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Employee
from promotion.models import PromotionInfo
from separation.models import SeparationInfo

from .serializers import EmployeeSerializer
from .serializers import EmployeeSerializer, PersonalInfoSerializer, EmploymentInfoSerializer, SalaryInfoSerializer 
from promotion.serializers import PromotionInfoSerializer 
from job_profile.serializers import JobProfileHistorySerializer 
from separation.serializers import SeparationInfoSerializer 
from transfer.serializers import TransferInfoSerializer


from HRCorp.permissions import IsPowerUserForModifyButStandardOrPowerUserForPOST




class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsPowerUserForModifyButStandardOrPowerUserForPOST]





class AllEmployeeInfoView(APIView):
    permission_classes = [IsPowerUserForModifyButStandardOrPowerUserForPOST]

    def get(self, request):
        # Fetch employees with related data     # via reverse relation
        employees = Employee.objects.prefetch_related(
            'personalinfo', 
            'employmentinfo', 
            'salaryinfo', 
            'separationinfo',
            'jobprofilehistory_set', 
            'promotioninfo_set', 
            'transferinfo_set'
        )

        combined_data = []

        for employee in employees:
            # personal informations
            personal_info = PersonalInfoSerializer(employee.personalinfo).data

            # employment related info
            employment_info = EmploymentInfoSerializer(employee.employmentinfo).data

            # salary informations
            # salary_info = SalaryInfoSerializer(employee.salaryinfo).data

            # Collect job profile history
            job_profile_history = JobProfileHistorySerializer(employee.jobprofilehistory_set.all(), many=True).data

            # Collect separation info
            try:
                separation_info = SeparationInfoSerializer(employee.separationinfo).data
            except SeparationInfo.DoesNotExist:
                separation_info = {}

            # Collect transfer info
            transfer_info = TransferInfoSerializer(employee.transferinfo_set.all(), many=True).data

            # Collect promotion info and get the last promotion
            promotions = PromotionInfo.objects.filter(employee=employee).order_by('-promotion_effective_date')
            last_promotion = PromotionInfoSerializer(promotions.first()).data if promotions.exists() else {}

            # Aggregate job profile details
            job_profile_details = ', '.join(
                [f"**{index + 1}.** {info['details']}" for index, info in enumerate(job_profile_history)]
            )

            combined_data.append({
                "employee_id": employee.employee_id,
                "personal_info": personal_info,
                "employment_info": employment_info,
                # "salary_info": salary_info,
                "job_profile_details": job_profile_details,
                "last_promotion": last_promotion,
                "separation_info": separation_info,
                "transfer_info": transfer_info,
            })

        return Response(combined_data)
    