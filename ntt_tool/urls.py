"""ntt_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ntt_tool.apps.core.urls')),
    url(r'^api/auth-token/', obtain_jwt_token),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('ntt_tool.apps.cloud.urls', namespace='api_cloud')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
