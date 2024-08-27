from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('power_user/', include('power_user.urls')),
    path('standard_user/', include('standard_user.urls')),

    path('employee/', include('employee.urls')),
    path('employment/', include('employment.urls')),
    path('salary/', include('salary.urls')),

    path('transfer/', include('transfer.urls')),
    path('confirmation/', include('confirmation.urls')),
    path('promotion/', include('promotion.urls')),
    path('separation/', include('separation.urls')),

    path('job_profile/', include('job_profile.urls')),
    
    # to implement authentication facility only in DRF panel
    path("api-auth/", include("rest_framework.urls")),
]

# adding onto the urlpatterns
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
