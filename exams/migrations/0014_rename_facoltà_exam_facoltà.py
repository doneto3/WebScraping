# Generated by Django 4.2 on 2023-04-19 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0013_alter_exam_semestre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='Facoltà',
            new_name='facoltà',
        ),
    ]
