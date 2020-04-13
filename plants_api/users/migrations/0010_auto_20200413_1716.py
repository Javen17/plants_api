# Generated by Django 2.2.5 on 2020-04-13 22:16

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200413_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='/home/javier/plants_api_project/plants_api/staticfiles/img/user-placeholder.png', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='uploads/perfiles', verbose_name='foto de perfil'),
        ),
    ]
