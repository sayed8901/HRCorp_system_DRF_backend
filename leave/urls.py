from django.urls import path

from .views import AllLeaveInfoDetailView, IndividualEmployeeLeaveInfoView, UpdateSingleLeaveInfoView, WithdrawSingleLeaveInfoView


urlpatterns = [
    path('list/', AllLeaveInfoDetailView.as_view(), name='all_employee_leave_info'),

    path('', IndividualEmployeeLeaveInfoView.as_view(), name='individual_employee_leave_info'),

    path('update/', UpdateSingleLeaveInfoView.as_view(), name='update_leave_info'),

    path('cancel/', WithdrawSingleLeaveInfoView.as_view(), name='delete_leave_info'),
]
