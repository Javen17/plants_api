# Generated by Django 2.2.5 on 2019-10-26 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_site', '0009_auto_20191019_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('number_id', models.PositiveIntegerField(unique=True, verbose_name='Número de referencia')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone', models.CharField(max_length=100, verbose_name='Teléfono')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/perfiles', verbose_name='foto de perfil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
        migrations.RemoveField(
            model_name='plantspecimen',
            name='recolector',
        ),
        migrations.DeleteModel(
            name='Recolector',
        ),
        migrations.AddField(
            model_name='plantspecimen',
            name='profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main_site.Profile', verbose_name='Perfil'),
        ),
    ]