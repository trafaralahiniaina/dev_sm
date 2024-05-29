from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Subject, ClassSchedule, Attendance, Note, Exam
from .serializers import SubjectSerializer, ClassScheduleSerializer, AttendanceSerializer, NoteSerializer, \
    ExamSerializer
from core.permissions import IsSiteAdmin, IsSchoolAdmin, IsTeacher


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSiteAdmin, IsSchoolAdmin, IsTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'code', 'school']


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsSiteAdmin, IsTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['value']


class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [IsAuthenticated, IsSiteAdmin, IsSchoolAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'grade', 'school']


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsSiteAdmin, IsSchoolAdmin, IsTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'section', 'school']


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsSchoolAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'section', 'school']
