# Generated by Django 5.0.1 on 2024-02-04 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstCarSogang_signuplogin', '0005_alter_normaluser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluser',
            name='sloworfast',
            field=models.BooleanField(default=True),
        ),
    ]
