# Generated by Django 5.0.1 on 2024-01-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstCarSogang_signuplogin', '0003_remove_normaluser_studentid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluser',
            name='username',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='서강대 학번'),
        ),
    ]
