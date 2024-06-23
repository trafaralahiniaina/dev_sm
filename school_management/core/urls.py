# school_management/core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SiteAdminViewSet, SchoolAdminViewSet, TeacherViewSet, ParentViewSet, StudentViewSet,
    CustomTokenObtainPairView, LogoutView
)

router = DefaultRouter()
router.register(r'site-admins', SiteAdminViewSet)
router.register(r'school-admins', SchoolAdminViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
