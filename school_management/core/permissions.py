# core/permissions.py


from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
from .models import SiteAdmin, SchoolAdmin, Teacher
from schools.models import School


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
    def has_object_permission(self, request, view, obj):
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

class IsSiteOrSchoolAdminOrReadOnlyForAll(permissions.BasePermission):
    def has_permission(self, request, view):
        # Autorise les requêtes GET, HEAD ou OPTIONS pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Vérifie si l'utilisateur est authentifié et s'il est un administrateur du site
        if request.user.is_authenticated and request.user.is_site_admin():
            return True

        # Vérifie si l'utilisateur est un administrateur d'école et si la requête concerne une école dont il est responsable
        if request.user.is_authenticated and request.user.is_school_admin():
            school_id = request.data.get('school') or request.query_params.get('school_id')
            if school_id and request.user.schooladmin.school.id == int(school_id):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        # Autorise les requêtes GET, HEAD ou OPTIONS pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Vérifie si l'utilisateur est un administrateur du site
        if request.user.is_authenticated and request.user.is_site_admin():
            return True

        # Vérifie si l'utilisateur est un administrateur d'école et si l'objet est lié à l'école dont il est responsable
        if request.user.is_authenticated and request.user.is_school_admin():
            if isinstance(obj, School) and obj == request.user.schooladmin.school:
                return True

        return False