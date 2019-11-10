# Generated by Django 2.2.5 on 2019-11-10 02:38

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0013_auto_20191109_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='biostatus',
            options={'verbose_name': 'Biostatus', 'verbose_name_plural': 'Biostatus'},
        ),
        migrations.AddField(
            model_name='mushroomspecimen',
            name='genus',
            field=smart_selects.db_fields.ChainedForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main_site.Genus', verbose_name='Género'),
        ),
        migrations.AddField(
            model_name='plantspecimen',
            name='genus',
            field=smart_selects.db_fields.ChainedForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main_site.Genus', verbose_name='Género'),
        ),
        migrations.AlterField(
            model_name='mushroomspecimen',
            name='species',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='genus', chained_model_field='genus', on_delete=django.db.models.deletion.CASCADE, to='main_site.Species'),
        ),
        migrations.AlterField(
            model_name='plantspecimen',
            name='species',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='genus', chained_model_field='genus', on_delete=django.db.models.deletion.CASCADE, to='main_site.Species'),
        ),
    ]
