# Generated by Django 5.0.5 on 2024-06-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_parent_parent_children_schools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='status',
            field=models.CharField(choices=[('couple', 'marié'), ('single_mom', 'mère célibataire'), ('single_dad', 'père célibataire'), ('tutor', 'tuteur')], default='NC', max_length=50),
        ),
    ]
