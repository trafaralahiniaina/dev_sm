# school_management/core/managers.py

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("L'adresse e-mail ou le numéro de téléphone est obligatoire")

        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Le super utilisateur doit avoir is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Le super utilisateur doit avoir is_superuser=True.")

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)

    def get_by_natural_key(self, username):
        try:
            return self.get(email=username)
        except self.model.DoesNotExist:
            return self.get(phone_number=username)