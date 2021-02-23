"""ThanksFinance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/", include("users.urls")),  # User Authentication API's
    path("api/", include("customers.urls")),  # Customer API's
    path("api/", include("stripAPI.urls")),  # Customer API's

]

schema_view = get_schema_view(
    openapi.Info(
        title="Thanks Finance",
        default_version='v1',
        description="Thanks Finance API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="codezilla.utsav@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r"^docs/", include_docs_urls(title="Thanks Finance")),
]

# http://localhost:8000/swagger.yaml
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
