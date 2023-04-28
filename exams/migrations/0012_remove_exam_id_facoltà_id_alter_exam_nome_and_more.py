# Generated by Django 4.2 on 2023-04-17 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_exam_id_alter_exam_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='id',
        ),
        migrations.AddField(
            model_name='facoltà',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
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
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='facoltà',
            constraint=models.UniqueConstraint(fields=('nome',), name='unique_migration_nome'),
        ),
    ]
