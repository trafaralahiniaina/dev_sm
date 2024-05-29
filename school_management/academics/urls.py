# school_management/academics/urls.py


from django.urls import path, include
from rest_framework import routers
from .views import SubjectViewSet, NoteViewSet, AttendanceViewSet, ClassScheduleViewSet, ExamViewSet

router = routers.DefaultRouter()
router.register('subject', SubjectViewSet, basename='subject')
router.register('note', NoteViewSet, basename='note')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('class-schedule', ClassScheduleViewSet, basename='class-schedule')
router.register('exam', ExamViewSet, basename='examen')

urlpatterns = [
    path('', include(router.urls)),
]
