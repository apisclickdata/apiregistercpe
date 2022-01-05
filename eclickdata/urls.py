from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Api Register CPE",
        default_version="V1",
        description="Api para gestionar CPE",
        terms_of_service="https://www.clickdata.pe",
        contact=openapi.Contact(email="apis@clickdata.pe"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
) 

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('adminapp/', include('register.urls')),
]
