# core/urls.py


from django.urls import path, include
from rest_framework import routers
from .views import (
    LogoutView, SiteAdminViewSet, SchoolAdminViewSet,
    TeacherViewSet, ParentViewSet, StudentViewSet, UserDetailView,
    UserProfilePictureChangeViewSet, CustomTokenObtainPairView
)

# Utilisation de DefaultRouter pour enregistrer les ViewSets
router = routers.DefaultRouter()
router.register('site-admins', SiteAdminViewSet, basename='site-admin')
router.register('school-admins', SchoolAdminViewSet, basename='school-admin')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('parents', ParentViewSet, basename='parent')
router.register('students', StudentViewSet, basename='student')
router.register('profile', UserProfilePictureChangeViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]