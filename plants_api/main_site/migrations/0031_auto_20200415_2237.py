# Generated by Django 2.2.5 on 2020-04-16 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0030_auto_20200413_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.City', verbose_name='Ciudad/Municipio'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.City', verbose_name='Ciudad/Municipio'),
        ),
    ]
