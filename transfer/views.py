from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TransferInfo
from .serializers import TransferInfoSerializer
from job_profile.models import JobProfileHistory
from employment.models import EmploymentInfo
from employee.models import Employee

# only power_user or standard_user can GET or PUT requests
from HRCorp.permissions import IsPowerOrStandardUserOtherwiseReadOnly
from power_user.permissions import IsPowerUserOrReadOnly



# Create your views here.
class AllTransferInfoDetailView(APIView):
    serializer_class = TransferInfoSerializer
    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]
    
    # both the standard_user and power_user can GET all the transfer info
    def get(self, request, format = None):
        transfers = TransferInfo.objects.all()
        serializer = TransferInfoSerializer(transfers, many=True)

        return Response(serializer.data)





# both the standard_user and power_user can GET or POST a transfer info
class IndividualEmployeeTransferInfoView(APIView):
    serializer_class = TransferInfoSerializer

    permission_classes = [IsPowerOrStandardUserOtherwiseReadOnly]


    
    # To get all the transfer information of an employee
    def get(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
            # print(employee)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)
        
        
        transfer_info_queryset = TransferInfo.objects.filter(employee = employee_id)
        
        serializer = TransferInfoSerializer(transfer_info_queryset, many=True)
        # print('transfer info:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    # To post transfer information
    def post(self, request, format = None):
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({'error': 'employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the employee instance from the employee_id
        try:
            employee = Employee.objects.get(employee_id = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)


        # Include the employee ID in the request_data to link it with the transfer record       # Use the employee instance's employee_id
        request_data = request.data.copy()
        request_data['employee'] = employee.employee_id


        serializer = TransferInfoSerializer(data = request_data)


        if serializer.is_valid():
            # getting the transfer information
            transfer_info = serializer.save(employee = employee)

            old_location = transfer_info.transfer_from_location
            old_department = transfer_info.transfer_from_department
            new_department = transfer_info.transfer_to_department
            new_location = transfer_info.transfer_to_location
            effect_date = transfer_info.transfer_effective_date.strftime("%d-%m-%Y")


            # Create a JobProfileHistory entry for "Transfer"
            JobProfileHistory.objects.create(
                employee = transfer_info.employee,
                event_type = 'Transfer',
                event_id = transfer_info.id,

                details=(
                    f'Transferred from {old_location} to {new_location} (from {old_department} to {new_department} dept.) with effect from {effect_date}.'
                ),
                effective_date = transfer_info.transfer_effective_date
            )


            # Update the current department and location in EmploymentInfo
            employment_info = EmploymentInfo.objects.get(employee = employee)
            employment_info.department = new_department
            employment_info.job_location = new_location
            
            employment_info.save()


            return Response(serializer.data)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# To update transfer information by power_user only
class UpdateSingleTransferInfoView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]


    # To update transfer information
    def put(self, request, format = None):
        transfer_id = request.query_params.get('transfer_id')

        if not transfer_id:
            return Response({'error': 'transfer_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch the specific transfer record using transfer_id
            transfer_info = TransferInfo.objects.get(id = transfer_id)
        except TransferInfo.DoesNotExist:
            return Response({'error': 'Transfer info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)
        

        request_data = request.data.copy()


        serializer = TransferInfoSerializer(transfer_info, data = request_data)


        if serializer.is_valid():
            transfer_info = serializer.save()

            old_location = transfer_info.transfer_from_location
            old_department = transfer_info.transfer_from_department
            new_department = transfer_info.transfer_to_department
            new_location = transfer_info.transfer_to_location
            effect_date = transfer_info.transfer_effective_date.strftime("%d-%m-%Y")

            # Update the existing JobProfileHistory entry
            job_profile_history = JobProfileHistory.objects.filter(
                employee = transfer_info.employee,
                event_type = 'Transfer',
            ).first()


            if job_profile_history:
                # update existing JobProfileHistory details & effective_date
                job_profile_history.details = (
                    f'Transferred from {old_location} to {new_location} (from {old_department} to {new_department} department) with effect from {effect_date}.'
                )
                job_profile_history.effective_date = transfer_info.transfer_effective_date

                job_profile_history.save()

            else:
                print("No JobProfileHistory found")


            # Update the current department and location in EmploymentInfo
            employment_info = EmploymentInfo.objects.get(employee = transfer_info.employee)

            employment_info.department = new_department
            employment_info.job_location = new_location
            
            employment_info.save()


            return Response(serializer.data)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# To delete the last transfer information by power_user only
class WithdrawSingleTransferInfoView(APIView):
    permission_classes = [IsPowerUserOrReadOnly]

    def delete(self, request, format=None):
        transfer_id = request.query_params.get('transfer_id')

        if not transfer_id:
            return Response({'error': 'transfer_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch the specific transfer record using transfer_id
            transfer_info = TransferInfo.objects.get(id = transfer_id)
        except TransferInfo.DoesNotExist:
            return Response({'error': 'Transfer info not found, may be incorrect employee ID given'}, status=status.HTTP_404_NOT_FOUND)


        # Capture current department and location before deletion
        present_location = transfer_info.transfer_to_location
        present_department = transfer_info.transfer_to_department


        employment_info = EmploymentInfo.objects.get(employee = transfer_info.employee)


        # Fetch the previous transfer record to restore department and location
        # Get the most recent transfer based on the transfer_effective_date.

        previous_transfer = TransferInfo.objects.filter(
            employee = transfer_info.employee,

            transfer_effective_date__lt=transfer_info.transfer_effective_date
        ).order_by('-transfer_effective_date').first()
        # '__lt' is a lookup type in Django that stands for "less than". 
        # It filters records to include only those where the transfer_effective_date is earlier than the provided date.
        

        if previous_transfer:
            restored_location = previous_transfer.transfer_to_location
            restored_department = previous_transfer.transfer_to_department
        else:
            # If no previous transfer, restoring the original department and location
            restored_location = transfer_info.transfer_from_location
            restored_department = transfer_info.transfer_from_department


        # Update the JobProfileHistory entry indicating the transfer was withdrawn
        JobProfileHistory.objects.create(
            employee = transfer_info.employee,
            event_type = 'Transfer_Withdraw',
            event_id = transfer_info.id,

            details = (
                f'Transfer withdrawn from {present_location} ({present_department} department) & continued at previous location: {restored_location} at {restored_department} department with effect from {transfer_info.transfer_effective_date}.'
            ),
            effective_date = transfer_info.entry_date
        )


        # Restore the department and location in EmploymentInfo
        employment_info.department = restored_department
        employment_info.job_location = restored_location

        employment_info.save()


        # Delete the transfer record
        transfer_info.delete()


        return Response({'message': 'Transfer information deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


