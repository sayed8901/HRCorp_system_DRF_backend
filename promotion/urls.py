from django.urls import path
from promotion.views import PromotionInfoCreateView, AllPromotionInfoDetailView


urlpatterns = [
    path('promote/', PromotionInfoCreateView.as_view(), name='promotion-create'),
    path('list/', AllPromotionInfoDetailView.as_view(), name='employment_info'),
]

