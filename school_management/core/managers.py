# core/managers.py

from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class SchoolQuerySet(models.QuerySet):
    def for_school(self, school):
        return self.filter(school=school)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class SchoolAdminManager(UserManager):
    def get_queryset(self):
        return SchoolQuerySet(self.model, using=self._db)

    def for_school(self, school):
        return self.get_queryset().for_school(school)


class TeacherManager(UserManager):
    def get_queryset(self):
        return SchoolQuerySet(self.model, using=self._db)

    def for_school(self, school):
        return self.get_queryset().for_school(school)


class StudentManager(UserManager):
    def get_queryset(self):
        return SchoolQuerySet(self.model, using=self._db)

    def for_school(self, school):
        return self.get_queryset().for_school(school)


class ParentManager(UserManager):
    def get_queryset(self):
        return SchoolQuerySet(self.model, using=self._db)

    def for_school(self, school):
        return self.get_queryset().for_school(school)