# Generated by Django 4.2 on 2023-04-17 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_remove_facoltà_unique_migration_nome_anno_semestre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
