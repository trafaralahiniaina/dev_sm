# Generated by Django 5.0.5 on 2024-05-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_teacher_teacher_schools_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='role',
        ),
        migrations.AddField(
            model_name='parent',
            name='father_first_name',
            field=models.CharField(default='NC', max_length=30),
        ),
        migrations.AddField(
            model_name='parent',
            name='father_job',
            field=models.CharField(default='NC', max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='father_last_name',
            field=models.CharField(default='NC', max_length=30),
        ),
        migrations.AddField(
            model_name='parent',
            name='mother_first_name',
            field=models.CharField(default='NC', max_length=30),
        ),
        migrations.AddField(
            model_name='parent',
            name='mother_job',
            field=models.CharField(default='NC', max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='mother_last_name',
            field=models.CharField(default='NC', max_length=30),
        ),
        migrations.AddField(
            model_name='parent',
            name='status',
            field=models.CharField(choices=[('couple', 'marié'), ('divorced', 'divorcés'), ('single_mom', 'mère célibataire'), ('single_dad', 'père célibataire'), ('tutor', 'tuteur')], default='NC', max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='tutor_first_name',
            field=models.CharField(default='NC', max_length=30),
        ),
        migrations.AddField(
            model_name='parent',
            name='tutor_job',
            field=models.CharField(default='NC', max_length=50),
        ),
        migrations.AddField(
            model_name='parent',
            name='tutor_last_name',
            field=models.CharField(default='NC', max_length=30),
        ),
    ]