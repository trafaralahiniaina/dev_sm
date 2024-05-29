from django.db import models
from django.utils import timezone
from core.models import SchoolAdmin


class SubscriptionPlan(models.Model):
    """
    Modèle pour représenter les différents plans d'abonnement.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text='Durée en mois')
    features = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Modèle pour représenter les abonnements des établissements scolaires.
    """
    schoolAdmin = models.ForeignKey(SchoolAdmin, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.schoolAdmin.email} - {self.plan.name}"
