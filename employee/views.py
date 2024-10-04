from rest_framework import viewsets
from .models import Employee

from .serializers import EmployeeSerializer

# only power_user can POST request but standard_user & power_user can GET, PUT or DELETE requests
from HRCorp.permissions import IsPowerUserForModifyButStandardOrPowerUserForPOST


# Create your views here.
class EmployeeViewSet(viewsets.ModelViewSet):
    # queryset = Employee.objects.all()
    queryset = Employee.objects.select_related(
        'personalinfo', 
        'employmentinfo', 
        'salaryinfo', 
        'separationinfo'
    )
    serializer_class = EmployeeSerializer

    permission_classes = [IsPowerUserForModifyButStandardOrPowerUserForPOST]
