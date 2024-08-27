from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PowerUserViewSet, PowerUserRegistrationAPIView, activate, PowerUserDataByUserIDView


# Create a router
router = DefaultRouter()

# register ViewSets with the router.
router.register('list', PowerUserViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    path('register/', PowerUserRegistrationAPIView.as_view(), name='power_user_register'),
    path('active/<user_id>/<token>/', activate, name='power_user_account_activate'),

    path('by_user_id/', PowerUserDataByUserIDView.as_view(), name='power_user_by_user_id'),
]

