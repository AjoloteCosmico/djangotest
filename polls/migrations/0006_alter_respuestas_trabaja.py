# Generated by Django 4.1.1 on 2022-09-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_respuestas_carrera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuestas',
            name='trabaja',
            field=models.BooleanField(default=False),
        ),
    ]
