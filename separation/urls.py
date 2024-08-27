from django.urls import path
from separation.views import SeparationInfoCreateView, AllSeparationInfoDetailView


urlpatterns = [
    path('deactivate/', SeparationInfoCreateView.as_view(), name='promotion-create'),
    path('list/', AllSeparationInfoDetailView.as_view(), name='employment_info'),
]

