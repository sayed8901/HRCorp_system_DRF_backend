from django.urls import path, include

from .views import SingleEmployeeJobProfileHistory, AllEmployeeJobProfileHistoryList


urlpatterns = [
    path('', SingleEmployeeJobProfileHistory.as_view(), name='job_profile_history'),
    path('list/', AllEmployeeJobProfileHistoryList.as_view(), name='job_profile_history'),
]

