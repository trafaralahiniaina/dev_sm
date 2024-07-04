# core/management/commands/list_active_school_admins.py
from django.core.management.base import BaseCommand
from core.models import SchoolAdmin


class Command(BaseCommand):
    help = "Liste tous les SchoolAdmins actifs"

    def handle(self, *args, **kwargs):
        active_school_admins = SchoolAdmin.objects.filter(is_active=True)

        if not active_school_admins.exists():
            self.stdout.write("Aucun SchoolAdmin actif trouvé.")
            return

        self.stdout.write("Liste des SchoolAdmins actifs :")
        for admin in active_school_admins:
            self.stdout.write(f" - {admin.first_name} {admin.last_name} ({admin.email})")
