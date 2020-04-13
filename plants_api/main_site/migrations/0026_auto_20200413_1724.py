# Generated by Django 2.2.5 on 2020-04-13 22:24

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0025_auto_20200413_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='photo',
            field=models.ImageField(default='/home/javier/plants_api_project/plants_api/staticfiles/img/default.jpg', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='uploads/specimen', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='photo',
            field=models.ImageField(default='/home/javier/plants_api_project/plants_api/staticfiles/img/default.jpg', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='uploads/specimen', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='species',
            name='photo',
            field=models.ImageField(default='/home/javier/plants_api_project/plants_api/staticfiles/img/default.jpg', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='uploads/plant_family', verbose_name='Imagen'),
        ),
    ]
