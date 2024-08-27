from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StandardUserViewSet, StandardUserRegistrationAPIView, activate, StandardUserDataByUserIDView


# Create a router
router = DefaultRouter()

# register ViewSets with the router.
router.register('list', StandardUserViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    path('register/', StandardUserRegistrationAPIView.as_view(), name='standard_user_register'),
    path('active/<user_id>/<token>/', activate, name='standard_user_account_activate'),

    path('by_user_id/', StandardUserDataByUserIDView.as_view(), name='standard_user_by_user_id'),
]

