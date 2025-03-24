from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    TaskViewSet,
    UserRegistrationView
)

app_name = 'TaskApp'

User = get_user_model()

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
]