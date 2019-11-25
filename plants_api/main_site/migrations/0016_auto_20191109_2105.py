# Generated by Django 2.2.5 on 2019-11-10 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0015_auto_20191109_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='aditional_info',
            field=models.TextField(blank=True, null=True, verbose_name='Información Adicional'),
        ),
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitud'),
        ),
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/specimen', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitud'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/specimen', verbose_name='Foto'),
        ),
    ]