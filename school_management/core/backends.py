from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.utils import timezone

from core.models import User, SiteAdmin, SchoolAdmin, Teacher, Parent, Student


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Essayez d'abord de trouver l'utilisateur par email
            user = User.objects.get(Q(email=username) | Q(phone_number=username) | Q(student_id=username))

            if check_password(password, user.password):
                # Déterminez le type d'utilisateur
                if isinstance(user, SiteAdmin):
                    user.user_type = "site_admin"
                elif isinstance(user, SchoolAdmin):
                    user.user_type = "school_admin"
                elif isinstance(user, Teacher):
                    user.user_type = "teacher"
                elif isinstance(user, Parent):
                    user.user_type = "parent"
                elif isinstance(user, Student):
                    user.user_type = "student"
                else:
                    user.user_type = "unknown"

                if user:
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                return user
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
