# Generated by Django 5.0.5 on 2024-06-23 14:03

import django.core.validators
import schools.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=schools.models.school_logo_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]),
        ),
    ]