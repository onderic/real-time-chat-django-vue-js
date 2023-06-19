from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # settings
    path('users/', api.user_data, name='user-detail'),
    path('user/<uuid:pk>/', api.user_info, name='user-info'),
    path('user_info_update/<uuid:pk>/', api.update_user, name='update-user'),

    # changepassword
     path('change_password/<uuid:pk>/', api.change_password, name='auth_change_password'),
]
