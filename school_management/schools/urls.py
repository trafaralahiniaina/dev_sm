# school_management/schools/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import SchoolViewSet, GradeViewSet, SectionViewSet, ClassRoomViewSet

router = routers.DefaultRouter()
router.register('schools', SchoolViewSet, basename='school')
router.register('grades', GradeViewSet, basename='grade')
router.register('sections', SectionViewSet, basename='section')
router.register('classrooms', ClassRoomViewSet, basename='classroom')

urlpatterns = [
    path('', include(router.urls)),
]
