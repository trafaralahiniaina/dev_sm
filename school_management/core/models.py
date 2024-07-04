# school_management/core/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db import models
from .managers import UserManager


def user_profile_picture_path(instance, filename):
    return f'profile_pictures/{instance.id}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="%(app_label)s_%(class)s_groups",
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="%(app_label)s_%(class)s_user_permissions",
        help_text='Specific permissions for this user.',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_user_type(self):
        if hasattr(self, 'siteadmin'):
            return 'site_admin'
        elif hasattr(self, 'schooladmin'):
            return 'school_admin'
        elif hasattr(self, 'teacher'):
            return 'teacher'
        elif hasattr(self, 'parent'):
            return 'parent'
        elif hasattr(self, 'student'):
            return 'student'
        return None

    def get_username(self):
        user_type = self.get_user_type()
        if user_type == 'site_admin' or user_type == 'school_admin':
            return self.email
        elif user_type == 'teacher' or user_type == 'parent':
            return str(self.phone_number)
        elif user_type == 'student':
            return str(self.student_id)
        return None


class SiteAdmin(User):
    role = models.CharField(max_length=50, choices=(
        ('admin', 'Administrateur'),
        ('developer', 'Développeur'),
        ('integrator', 'Intégrateur'),
        ('moderator', 'Modérateur'),
    ))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class SchoolAdmin(User):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='admins')
    role = models.CharField(max_length=50, choices=(
        ('school_admin', 'Administrateur d\'école'),
        ('content_integrator', 'Intégrateur de contenu'),
        ('moderator', 'Modérateur'),
        ('staff', 'Personnel'),
        ('proviseur', 'Proviseur '),
        ('censeur', 'Censeur '),
        ('adjoint', 'Adjoint au proviseur'),
        ('chef_de_travaux', 'Chef de travaux'),
        ('Responsable_d_équipe_pédagogique', 'Responsable d\'équipe pédagogique '),
        ('directeur', 'Directeur '),
        ('chef_de_département', 'Chef de département '),
        ('Conseiller_principal_d_éducation', 'Conseiller principal d\'éducation '),
    ))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'school']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.school.name} ({self.role})"


class Teacher(User):
    teacher_schools = models.ManyToManyField('schools.Section', related_name='teachers', blank=True, null=True)
    teacher_subjects = models.ManyToManyField('academics.Subject', related_name='teachers', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Enseignant"


class Parent(User):
    parent_children_schools = models.ManyToManyField('schools.School', related_name='parents', blank=True, null=True)
    address = models.CharField(max_length=200, null=True)

    status = models.CharField(max_length=50, choices=(
        ('couple', 'marié'),
        ('single_mom', 'mère célibataire'),
        ('single_dad', 'père célibataire'),
        ('tutor', 'tuteur')
    ), default='NC')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'status']

    def __str__(self):
        return f"{self.phone_number} - Parent (Status: {self.status})"


class Student(User):
    student_number_sections = models.IntegerField(default=0)
    student_sex = models.CharField(max_length=20, choices=(('male', 'garçon'), ('female', 'fille')), default='NC')
    grade_level = models.ForeignKey('schools.Grade', on_delete=models.CASCADE, related_name='students')
    section = models.ForeignKey('schools.Section', on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='students')
    student_parent = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='students', blank=True,
                                       null=True)
    address = models.CharField(max_length=200)

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'grade_level', 'section', 'school']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Étudiant ({self.student_id})"
