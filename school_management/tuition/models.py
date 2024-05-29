from django.db import models
from core.models import Student, User


class TuitionFee(models.Model):
    """
    Modèle pour représenter les frais de scolarité.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    academic_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class StudentTuitionFee(models.Model):
    """
    Modèle pour lier un étudiant à un frais de scolarité spécifique.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tuition_fees')
    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.PROTECT, related_name='student_fees')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.tuition_fee.name}"
