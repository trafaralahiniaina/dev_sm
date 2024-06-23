# schools/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from core.permissions import IsSiteOrSchoolAdminOrReadOnlyForAll
from .models import School, Grade, Section, ClassRoom
from .serializers import SchoolSerializer, GradeSerializer, SectionSerializer, ClassRoomSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnlyForAll]

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id', None)
        if school_id:
            return self.queryset.filter(id=school_id)
        return self.queryset


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnlyForAll]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnlyForAll]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnlyForAll]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()