from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views 
app_name = 'authentication'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    

     path('api/protected/', views.protected_view, name='protected'),
    # JWT Token routes (for getting and refreshing tokens)
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]