"""Urls.py."""
from django.urls import include, path
from djoser.views import TokenCreateView
from rest_framework.routers import DefaultRouter

from .views import CustomTokenDestroyView, CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', CustomUserViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('', include('djoser.urls')),
     path('auth/', include('djoser.urls.authtoken')),
     path('auth/token/login/',
          TokenCreateView.as_view(),
          name='login'),
     path('auth/token/logout/',
          CustomTokenDestroyView.as_view(),
          name='logout'),
     path('auth/users/set_password/',
          CustomTokenDestroyView.as_view(),
          name='change_password'),
]
