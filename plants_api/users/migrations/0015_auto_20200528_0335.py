# Generated by Django 2.2.5 on 2020-05-28 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200515_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo_url',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='/home/javier/plants_api_project/plants_api/staticfiles/img/user-placeholder.png', null=True, upload_to='uploads/perfiles', verbose_name='foto de perfil'),
        ),
    ]
