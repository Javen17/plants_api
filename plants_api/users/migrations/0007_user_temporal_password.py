# Generated by Django 2.2.5 on 2020-03-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20191026_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temporal_password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Temporal Password'),
        ),
    ]
