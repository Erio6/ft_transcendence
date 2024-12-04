from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include(tf_urls)),
    path('admin/', admin.site.urls),  # Admin route
    path('', views.home, name="home"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('authentication.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include('user.urls')),
    path('auth/', include('authentication.urls')),
    path('friends/', include('friends.urls')),
]

# only for production to change for deploying
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
