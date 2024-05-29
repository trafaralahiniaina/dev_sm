# schools/models.py

from django.db import models


def school_logo_path(instance, filename):
    """
    Définit le chemin du fichier du logo de l'école.
    """
    return f'logos/{instance.id}/{filename}'


class School(models.Model):
    """
    Modèle représentant une école.
    """
    name = models.CharField(max_length=100, unique=True)
    sigle = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(upload_to=school_logo_path, null=True, blank=True)
    slogan = models.CharField(max_length=255, default='NC')  # Ajout du champ slogan avec une valeur par défaut
    address = models.CharField(max_length=200)
    commune = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    """
    Modèle représentant un niveau scolaire.
    """
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('academics.Subject', related_name='grades', null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grades')

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Section(models.Model):
    """
    Modèle représentant une section/classe d'un niveau scolaire.
    """
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # Ajout du champ academic_year

    def __str__(self):
        return f"{self.name} ({self.grade.name}, {self.grade.school.name}, {self.academic_year})"


class ClassRoom(models.Model):
    """
    Modèle représentant une salle de classe.
    """
    name = models.CharField(max_length=50)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return f"{self.name} ({self.section.name}, {self.section.grade.school.name})"
