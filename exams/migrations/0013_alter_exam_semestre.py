# Generated by Django 4.2 on 2023-04-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0012_remove_exam_id_facoltà_id_alter_exam_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='semestre',
            field=models.IntegerField(choices=[(1, '1° Semestre'), (2, '2° Semestre'), (3, 'Ciclo Annuale Unico')]),
        ),
    ]
