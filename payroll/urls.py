from django.urls import path, include
from .views import PayrollListCreateAPIView, PayrollRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('process_payroll/', PayrollListCreateAPIView.as_view(), name='process_payroll'),

    path('payroll/<int:pk>/', PayrollRetrieveUpdateDestroyAPIView.as_view(), name='payroll-detail'),
]
