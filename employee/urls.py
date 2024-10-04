from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AllEmployeeInfoView


router = DefaultRouter()
router.register('list', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all-info/', AllEmployeeInfoView.as_view(), name='all_employee_info'),
]
