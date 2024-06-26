# Generated by Django 5.0.5 on 2024-05-11 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_initial'),
        ('schools', '0002_rename_city_school_region_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='date',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='max_value',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='school',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('absent', 'Absent'), ('late', 'En retard')], max_length=20),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('coefficient', models.IntegerField(default=1)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='schools.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='academics.subject')),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='academics.exam'),
        ),
    ]
