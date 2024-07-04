# Créer un SchoolAdmin via un script Python
from core.models import SchoolAdmin
from schools.models import School

school = School.objects.get(id=1)  # Obtenir une école existante
school_admin = SchoolAdmin(
    email='admin@school.com',
    first_name='Admin',
    last_name='School',
    school=school,
    role='school_admin',
    is_active=True,
    is_staff=True
)
school_admin.set_password('password123')
school_admin.save()
