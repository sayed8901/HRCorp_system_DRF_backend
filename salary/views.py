from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SalaryInfo
from .serializers import SalaryInfoSerializer

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly



# Create your views here.
class AllSalaryInfoDetailView(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    serializer_class = SalaryInfoSerializer
    
    # both the standard_user and power_user can GET all the transfer info
    def get(self, request, format = None):
        salary_data = SalaryInfo.objects.all()
        serializer = SalaryInfoSerializer(salary_data, many=True)

        return Response(serializer.data)
    




class SalaryInfoDetail(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    def get(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            salary_info = SalaryInfo.objects.get(employee = employee_id)
        except SalaryInfo.DoesNotExist:
            return Response({'error': 'Salary info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SalaryInfoSerializer(salary_info)
        print('salary info:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    def put(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            salary_info = SalaryInfo.objects.get(employee = employee_id)
        except SalaryInfo.DoesNotExist:
            return Response({'error': 'Salary info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SalaryInfoSerializer(salary_info, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


