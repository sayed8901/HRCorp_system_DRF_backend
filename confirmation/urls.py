from django.urls import path
from confirmation.views import ConfirmationInfoCreateView, AllConfirmationInfoDetailView


urlpatterns = [
    path('confirm/', ConfirmationInfoCreateView.as_view(), name='confirmation-create'),
    path('list/', AllConfirmationInfoDetailView.as_view(), name='employment_info'),
]

