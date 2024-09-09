from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from employee.models import Employee
from .models import Leave
from .serializers import LeaveSerializer

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly
from power_user.permissions import IsPowerUserOrReadOnly



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
            employee = Employee.objects.get(employee_id=employee_id)
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
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)


        # Include the employee ID in the request_data to link it with the leave record       # Use the employee instance's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id


        serializer = LeaveSerializer(data=request_data)


        if serializer.is_valid():
            # getting the leave information
            leave = serializer.save(employee=employee)

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
            leave = Leave.objects.get(id=leave_id)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave info not found, may be incorrect leave ID given'}, status=status.HTTP_404_NOT_FOUND)


        serializer = LeaveSerializer(leave, data=request.data, partial=True)

        if serializer.is_valid():
            leave = serializer.save()
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

        leave.delete()
        
        return Response({'message': 'Leave information deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



