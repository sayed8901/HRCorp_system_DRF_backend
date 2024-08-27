from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import JobProfileHistory
from .serializers import JobProfileHistorySerializer

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly



# Create your views here.
class JobProfileHistoryDetail(APIView):
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    def get(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        job_profile_history_info = JobProfileHistory.objects.filter(employee = employee_id)
        
        serializer = JobProfileHistorySerializer(job_profile_history_info, many=True)
        print('job profile history:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
