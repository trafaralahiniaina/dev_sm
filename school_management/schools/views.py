# schools/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import Http404
from core.permissions import IsSiteOrSchoolAdminOrReadOnlyForAll
from .models import School, Grade, Section, ClassRoom
from .serializers import SchoolSerializer, GradeSerializer, SectionSerializer, ClassRoomSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnlyForAll]
    lookup_field = 'sigle'

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id', None)
        if school_id:
            return self.queryset.filter(id=school_id)
        return self.queryset

    def get_object(self):
        sigle = self.kwargs.get(self.lookup_field, '').upper()
        try:
            return School.objects.get(sigle__iexact=sigle)
        except School.DoesNotExist:
            raise Http404('No School matches the given query.')

    @action(detail=False, methods=['get'], url_path='list')
    def list_schools(self, request):
        schools = self.get_queryset()
        serializer = self.get_serializer(schools, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='details')
    def school_details(self, request, sigle=None):
        school = self.get_object()
        serializer = self.get_serializer(school)
        return Response(serializer.data)


@api_view(['GET'])
def get_school_by_sigle(request, sigle):
    try:
        school = School.objects.get(sigle__iexact=sigle)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)
    except School.DoesNotExist:
        return Response({'detail': 'No School matches the given query.'}, status=status.HTTP_404_NOT_FOUND)


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