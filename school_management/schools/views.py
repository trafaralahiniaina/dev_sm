# schools/views.py

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from core.permissions import IsSiteAdmin, IsSiteOrSchoolAdminOrReadOnly
from .models import School, Grade, Section, ClassRoom
from .serializers import SchoolSerializer, GradeSerializer, SectionSerializer, ClassRoomSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsSiteAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id', None)
        if school_id:
            return self.queryset.filter(id=school_id)
        return self.queryset


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]
