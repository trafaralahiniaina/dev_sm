# school_management/core/views.py

from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SiteAdmin, SchoolAdmin, Teacher, Parent, Student
from .serializers import (
    SiteAdminSerializer, SchoolAdminSerializer, TeacherSerializer, ParentSerializer, StudentSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AuthLoginSerializer
from rest_framework.request import Request
from django.utils.functional import empty
from core.serializers import clean_input
from django.contrib.auth import logout
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthLoginSerializer

    def post(self, request: Request, *args, **kwargs):
        # Créer une copie mutable de request.data
        mutable_data = request.data.copy()

        # Nettoyer le username
        if 'username' in mutable_data:
            mutable_data['username'] = clean_input(mutable_data['username'])

        # Créer une nouvelle Request avec les données nettoyées
        clean_request = Request(
            request._request,
            parsers=request.parsers,
            authenticators=request.authenticators,
            negotiator=request.negotiator,
            parser_context=request.parser_context
        )
        clean_request._full_data = mutable_data
        clean_request._data = empty

        # Appeler la méthode post de la classe parente avec la nouvelle requête
        return super().post(clean_request, *args, **kwargs)


class SiteAdminViewSet(viewsets.ModelViewSet):
    queryset = SiteAdmin.objects.all()
    serializer_class = SiteAdminSerializer


class SchoolAdminViewSet(viewsets.ModelViewSet):
    queryset = SchoolAdmin.objects.all()
    serializer_class = SchoolAdminSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Django's logout function is used here for session logout, but JWT tokens are managed client-side
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)