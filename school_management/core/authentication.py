from django.contrib.auth.backends import ModelBackend
from .models import SiteAdmin, SchoolAdmin, Teacher, Parent, Student


class SiteAdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = SiteAdmin.objects.get(email=username)
        except SiteAdmin.DoesNotExist:
            return None

        if user and user.check_password(password):
            user.user_type = "site_admin"
            return user
        return None


class SchoolAdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = SchoolAdmin.objects.get(email=username)
        except SchoolAdmin.DoesNotExist:
            return None

        if user and user.check_password(password):
            user.user_type = "school_admin"
            return user
        return None


class TeacherBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Teacher.objects.get(phone_number=username)
        except Teacher.DoesNotExist:
            return None

        if user and user.check_password(password):
            user.user_type = "teacher"
            return user
        return None


class ParentBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Parent.objects.get(phone_number=username)
        except Parent.DoesNotExist:
            return None

        if user and user.check_password(password):
            user.user_type = "parent"
            return user
        return None


class StudentBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Student.objects.get(student_id=username)
        except Student.DoesNotExist:
            return None

        if user and user.check_password(password):
            user.user_type = "student"
            return user
        return None
