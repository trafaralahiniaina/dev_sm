# school_management/academics/models.py

from django.db import models
from core.models import Student, Teacher
from schools.models import School, Section


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ClassSchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_schedules')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='class_schedules')
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.PositiveSmallIntegerField(
        choices=[(1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi'),
                 (7, 'Dimanche')])


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20,
                              choices=[('absent', 'Absent'), ('late', 'En retard')])


class Exam(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='exams')
    coefficient = models.IntegerField(default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.section} - {self.section.grade.school.name}"


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades', null=True)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField()
