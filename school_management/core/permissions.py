# core/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsSiteAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'siteadmin')

class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'schooladmin')

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'teacher')

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

class IsSiteOrSchoolAdminOrReadOnlyForAll(permissions.BasePermission):
    """
    Autorise tout le monde à lire, même sans authentification.
    Seuls les administrateurs du site et d'école peuvent créer, modifier ou supprimer.
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
        return request.user.is_authenticated and hasattr(request.user, 'parent')

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'student')