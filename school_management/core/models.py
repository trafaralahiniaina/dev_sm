# school_management/core/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db import models
from .managers import UserManager


def user_profile_picture_path(instance, filename):
    """
    Fonction pour définir le chemin du fichier de la photo de profil de l'utilisateur.
    """
    return f'profile_pictures/{instance.id}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle de base pour les utilisateurs dans le système.
    Hérite de AbstractBaseUser et PermissionsMixin pour la gestion des autorisations.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Champs pour la gestion des groupes et des permissions
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_site_admin(self):
        return hasattr(self, 'siteadmin')

    def is_school_admin(self):
        return hasattr(self, 'schooladmin')

    def is_teacher(self):
        return hasattr(self, 'teacher')

    def is_parent(self):
        return hasattr(self, 'parent')

    def is_student(self):
        return hasattr(self, 'student')


class SiteAdmin(User):
    """
    Modèle pour les administrateurs du site.
    Hérite du modèle User et ajoute un champ pour le rôle.
    """
    role = models.CharField(max_length=50, choices=(
        ('admin', 'Administrateur'),
        ('developer', 'Développeur'),
        ('integrator', 'Intégrateur'),
        ('moderator', 'Modérateur'),
    ))

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class SchoolAdmin(User):
    """
    Modèle pour les administrateurs d'école.
    Hérite du modèle User et ajoute une relation avec l'école et un champ pour le rôle.
    """
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='admins')
    role = models.CharField(max_length=50, choices=(
        ('school_admin', 'Administrateur d\'école'),
        ('content_integrator', 'Intégrateur de contenu'),
        ('moderator', 'Modérateur'),
        ('staff', 'Personnel'),
        ('proviseur ', 'Proviseur '),
        ('censeur ', 'Censeur '),
        ('adjoint', 'Adjoint au proviseur'),
        ('chef_de_travaux', 'Chef de travaux'),
        ('Responsable_d_équipe_pédagogique ', 'Responsable d\'équipe pédagogique '),
        ('directeur ', 'Directeur '),
        ('chef_de_département ', 'Chef de département '),
        ('Conseiller_principal_d_éducation ', 'Conseiller principal d\'éducation '),
    ))

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.school.name} ({self.role})"


class Teacher(User):
    """
    Modèle pour les enseignants.
    Hérite du modèle User et ajoute des relations avec les écoles et les matières enseignées.
    """
    teacher_schools = models.ManyToManyField('schools.Section', related_name='teachers')
    teacher_subjects = models.ManyToManyField('academics.Subject', related_name='teachers')
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Enseignant"


# school_management/core/models.py

class Parent(User):
    """
    Modèle pour les parents.
    Hérite du modèle User et ajoute des relations avec les écoles de leurs enfants.
    """
    phone_number = models.CharField(max_length=20, unique=True)
    parent_children_schools = models.ManyToManyField('schools.School', related_name='parents')
    address = models.CharField(max_length=200, null=True)

    # Statut familial
    status = models.CharField(max_length=50, choices=(
        ('couple', 'marié'),
        ('divorced', 'divorcés'),
        ('single_mom', 'mère célibataire'),
        ('single_dad', 'père célibataire'),
        ('tutor', 'tuteur')
    ), default='NC')

    # Informations sur la mère
    mother_first_name = models.CharField(max_length=30, default='NC')
    mother_last_name = models.CharField(max_length=30, default='NC')
    mother_job = models.CharField(max_length=50, default='NC')

    # Informations sur le père
    father_first_name = models.CharField(max_length=30, default='NC')
    father_last_name = models.CharField(max_length=30, default='NC')
    father_job = models.CharField(max_length=50, default='NC')

    # Informations sur le tuteur
    tutor_first_name = models.CharField(max_length=30, default='NC')
    tutor_last_name = models.CharField(max_length=30, default='NC')
    tutor_job = models.CharField(max_length=50, default='NC')

    def __str__(self):
        return f"{self.phone_number} - Parent (Status: {self.status})"


class Student(User):
    """

    Modèle pour les étudiants.
    Hérite du modèle User et ajoute des relations avec l'école, le niveau, la section et le parent.
    """
    student_id = models.CharField(max_length=20, unique=True)
    student_number_sections = models.IntegerField(default=0)
    student_sex = models.CharField(max_length=20, null=True, choices=(('male', 'garçon'), ('female', 'fille')),
                                   default='NC')
    grade_level = models.ForeignKey('schools.Grade', on_delete=models.CASCADE, related_name='students')
    section = models.ForeignKey('schools.Section', on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='students')
    student_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    address = models.CharField(max_length=200)

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'grade_level', 'section']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Étudiant ({self.student_id})"
