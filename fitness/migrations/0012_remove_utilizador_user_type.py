# Generated by Django 5.0.4 on 2024-05-09 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0011_alter_utilizador_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilizador',
            name='user_type',
        ),
    ]
