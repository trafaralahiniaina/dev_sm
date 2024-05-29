# core/permissions.py


from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
from .models import SiteAdmin, SchoolAdmin, Teacher


class IsSiteAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            isinstance(user, SiteAdmin)
        )


class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            isinstance(user, SchoolAdmin)
        )


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            isinstance(user, Teacher)
        )


class IsSiteOrSchoolAdminOrReadOnly(permissions.BasePermission):
    """
    Autorise les administrateurs du site et d'école à modifier, mais autorise tout le monde à lire.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
                hasattr(request.user, 'siteadmin') or hasattr(request.user, 'schooladmin')
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_parent()


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student()
