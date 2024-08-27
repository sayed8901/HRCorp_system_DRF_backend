from django.urls import path, include

from .views import SalaryInfoDetail, AllSalaryInfoDetailView


urlpatterns = [
    path('salary_info/', SalaryInfoDetail.as_view(), name='salary_info'),
    path('salary_info/list/', AllSalaryInfoDetailView.as_view(), name='all_salary_info'),
]
