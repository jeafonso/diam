# Generated by Django 5.0.4 on 2024-05-09 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0012_remove_utilizador_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilizador',
            name='user_type',
            field=models.CharField(choices=[('cliente', 'CLIENTE'), ('funcionario', 'FUNCIONARIO')], default='cliente', max_length=20),
            preserve_default=False,
        ),
    ]
