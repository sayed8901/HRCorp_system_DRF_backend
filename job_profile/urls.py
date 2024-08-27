from django.urls import path, include

from .views import JobProfileHistoryDetail


urlpatterns = [
    path('history/', JobProfileHistoryDetail.as_view(), name='job_profile_history'),
]

