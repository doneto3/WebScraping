# Generated by Django 4.2 on 2023-04-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0009_exam_facoltà_unique_migration_nome_anno_semestre_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='facoltà',
            name='unique_migration_nome_anno_semestre',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='id',
        ),
        migrations.RemoveField(
            model_name='facoltà',
            name='anno',
        ),
        migrations.RemoveField(
            model_name='facoltà',
            name='id',
        ),
        migrations.RemoveField(
            model_name='facoltà',
            name='semestre',
        ),
        migrations.AddField(
            model_name='exam',
            name='anno',
            field=models.IntegerField(choices=[(1, 'Primo Anno'), (2, 'Secondo Anno'), (3, 'Terzo Anno')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='semestre',
            field=models.IntegerField(choices=[(1, '1° Semestre'), (2, '2° Semestre')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='nome',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='facoltà',
            name='nome',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
