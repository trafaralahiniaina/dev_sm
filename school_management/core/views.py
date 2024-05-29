# core/views.py


from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
from core.permissions import IsSiteAdmin, IsSchoolAdmin, IsOwnerOrReadOnly, IsSiteOrSchoolAdminOrReadOnly
from core.models import SiteAdmin, SchoolAdmin, Teacher, Parent, Student, User
from core.serializers import (
    SiteAdminSerializer, SchoolAdminSerializer, TeacherSerializer,
    ParentSerializer, StudentSerializer, UserSerializer,
    TokenObtainSerializer, StudentPasswordSerializer
)
from core.mixins import ProfilePictureMixin, ChangePasswordMixin
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Custom Token Obtain Pair View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


# User Detail View for logged-in user's info
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Base Admin ViewSet with common settings for admin types
class BaseAdminViewSet(ProfilePictureMixin, ChangePasswordMixin, viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [IsSiteAdmin()]
        elif self.action == 'destroy':
            return [IsSiteAdmin()]
        elif self.action in ['update', 'partial_update', 'upload_profile_picture', 'change_password']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()


# Base User ViewSet with common settings for all user types
class BaseUserViewSet(ProfilePictureMixin, ChangePasswordMixin, viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsSiteOrSchoolAdminOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [IsSiteAdmin(), IsSchoolAdmin()]
        elif self.action == 'destroy':
            return [IsSiteAdmin(), IsSchoolAdmin()]
        elif self.action in ['update', 'partial_update', 'upload_profile_picture', 'change_password']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()


# SiteAdmin ViewSet
class SiteAdminViewSet(BaseAdminViewSet):
    queryset = SiteAdmin.objects.all()
    serializer_class = SiteAdminSerializer
    password_serializer_class = StudentPasswordSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsSiteAdmin()]
        return [AllowAny()]


# SchoolAdmin ViewSet
class SchoolAdminViewSet(BaseAdminViewSet):
    queryset = SchoolAdmin.objects.all()
    serializer_class = SchoolAdminSerializer
    password_serializer_class = StudentPasswordSerializer


# Teacher ViewSet
class TeacherViewSet(BaseUserViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    password_serializer_class = StudentPasswordSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'siteadmin'):
            return Teacher.objects.all()
        elif hasattr(user, 'schooladmin'):
            return Teacher.objects.filter(teacher_schools__school=user.schooladmin.school)
        elif hasattr(user, 'teacher'):
            return Teacher.objects.filter(id=user.id)
        return Teacher.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsSchoolAdmin()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()


# Parent ViewSet
class ParentViewSet(BaseUserViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    password_serializer_class = StudentPasswordSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'siteadmin'):
            return Parent.objects.all()
        elif hasattr(user, 'schooladmin'):
            return Parent.objects.filter(parent_children_schools=user.schooladmin.school)
        elif hasattr(user, 'parent'):
            return Parent.objects.filter(id=user.id)
        return Parent.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsSchoolAdmin()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()


# Student ViewSet
class StudentViewSet(BaseUserViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    password_serializer_class = StudentPasswordSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'siteadmin'):
            return Student.objects.all()
        elif hasattr(user, 'schooladmin'):
            return Student.objects.filter(school=user.schooladmin.school)
        elif hasattr(user, 'teacher'):
            return Student.objects.filter(section__in=user.teacher.teacher_schools.all())
        elif hasattr(user, 'parent'):
            return Student.objects.filter(student_parent=user.parent)
        return Student.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsSchoolAdmin()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()


# UserProfilePictureChangeViewSet for managing user profiles
class UserProfilePictureChangeViewSet(ProfilePictureMixin, ChangePasswordMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    password_serializer_class = StudentPasswordSerializer

    def get_permissions(self):
        # Customize permissions based on action
        if self.action in ['upload_profile_picture', 'change_password']:
            # Only authenticated users can change their password or upload a profile picture
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            # For other actions, use the standard permission checks
            return [IsOwnerOrReadOnly()]
        return [AllowAny()]


# LoginView using JWT for token creation
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainSerializer


# LogoutView for user logout
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Django's logout function is used here for session logout, but JWT tokens are managed client-side
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
