# Generated by Django 2.2.5 on 2020-04-13 22:04

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200328_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='/static/img/user-placeholder.png', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='uploads/perfiles', verbose_name='foto de perfil'),
        ),
    ]
