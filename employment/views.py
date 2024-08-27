from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PersonalInfo, EmploymentInfo, Department, Designation, JobLocation
from .serializers import PersonalInfoSerializer, EmploymentInfoSerializer, DepartmentSerializer, DesignationSerializer, JobLocationSerializer
from power_user.permissions import IsPowerUserOrReadOnly

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly



# Create your views here.
class AllPersonalInfoDetailView(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    serializer_class = PersonalInfoSerializer
    
    # both the standard_user and power_user can GET all the transfer info
    def get(self, request, format = None):
        transfers = PersonalInfo.objects.all()
        serializer = PersonalInfoSerializer(transfers, many=True)

        return Response(serializer.data)





class PersonalInfoDetail(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    def get(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            personal_info = PersonalInfo.objects.get(employee = employee_id)
        except PersonalInfo.DoesNotExist:
            return Response({'error': 'Personal info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PersonalInfoSerializer(personal_info)
        print('personal info:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    def put(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            personal_info = PersonalInfo.objects.get(employee = employee_id)
        except PersonalInfo.DoesNotExist:
            return Response({'error': 'Personal info not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalInfoSerializer(personal_info, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AllEmploymentInfoDetailView(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    serializer_class = EmploymentInfoSerializer
    
    # both the standard_user and power_user can GET all the transfer info
    def get(self, request, format = None):
        transfers = EmploymentInfo.objects.all()
        serializer = EmploymentInfoSerializer(transfers, many=True)

        return Response(serializer.data)





class EmploymentInfoDetail(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    def get(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employment_info = EmploymentInfo.objects.get(employee = employee_id)
        except EmploymentInfo.DoesNotExist:
            return Response({'error': 'Employment info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmploymentInfoSerializer(employment_info)
        print('employment info:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    def put(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employment_info = EmploymentInfo.objects.get(employee = employee_id)
        except EmploymentInfo.DoesNotExist:
            return Response({'error': 'Employment info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmploymentInfoSerializer(employment_info, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    permission_classes = [IsPowerUserOrReadOnly]





class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

    permission_classes = [IsPowerUserOrReadOnly]





class JobLocationViewSet(viewsets.ModelViewSet):
    queryset = JobLocation.objects.all()
    serializer_class = JobLocationSerializer

    permission_classes = [IsPowerUserOrReadOnly]

