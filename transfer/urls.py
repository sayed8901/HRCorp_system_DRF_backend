from django.urls import path, include

from .views import AllTransferInfoDetailView, IndividualEmployeeTransferInfoView, UpdateSingleTransferInfoView, WithdrawSingleTransferInfoView


urlpatterns = [
    path('list/', AllTransferInfoDetailView.as_view(), name='all_employee_transfer_info'),

    path('', IndividualEmployeeTransferInfoView.as_view(), name='individual_employee_transfer_info'),

    path('update/', UpdateSingleTransferInfoView.as_view(), name='update_transfer_info'),

    path('cancel/', WithdrawSingleTransferInfoView.as_view(), name='delete_transfer_info'),
]
