# Generated by Django 5.0.4 on 2024-05-10 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0013_utilizador_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilizador',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_pfp.jpg', upload_to='profile_pictures/'),
        ),
    ]
