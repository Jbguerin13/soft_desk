from django.urls import path
from rest_framework.routers import DefaultRouter
from  users.views import UserViewSet, RegisterUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls + [
    path('register/', RegisterUserView.as_view(), name='register_user'),
]