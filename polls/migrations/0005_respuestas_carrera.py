# Generated by Django 4.1.1 on 2022-09-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_respuestas_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestas',
            name='carrera',
            field=models.CharField(default='000', max_length=3),
        ),
    ]
