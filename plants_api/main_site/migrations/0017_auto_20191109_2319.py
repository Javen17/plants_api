# Generated by Django 2.2.5 on 2019-11-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0016_auto_20191109_2105'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CapTypes',
            new_name='CapType',
        ),
        migrations.RenameModel(
            old_name='FormTypes',
            new_name='FormType',
        ),
        migrations.AlterModelOptions(
            name='recolectionareastatus',
            options={'verbose_name': 'Descripción del habitad', 'verbose_name_plural': 'Descripciónes del habitad'},
        ),
        migrations.AlterField(
            model_name='recolectionareastatus',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Descripción del habitad'),
        ),
    ]
