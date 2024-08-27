from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PersonalInfoDetail, AllPersonalInfoDetailView, EmploymentInfoDetail, AllEmploymentInfoDetailView, DepartmentViewSet, DesignationViewSet, JobLocationViewSet


router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('designations', DesignationViewSet)
router.register('job_locations', JobLocationViewSet)



urlpatterns = [
    path('', include(router.urls)),

    path('personal_info/', PersonalInfoDetail.as_view(), name='personal_info'),
    path('personal_info/list/', AllPersonalInfoDetailView.as_view(), name='all_personal_info'),

    path('employment_info/', EmploymentInfoDetail.as_view(), name='employment_info'),
    path('employment_info/list/', AllEmploymentInfoDetailView.as_view(), name='employment_info'),
]


