from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from plants_api.users.models import User
# Create your models here.

class PlantFamily(models.Model):
    family_name = models.CharField(max_length=100 , verbose_name="Nombre de la familia" , unique = True)

    class Meta:
        verbose_name = 'Familias de plantas'
        verbose_name_plural = 'Familias de plantas'

    def __str__(self):
        return "%s" % (self.family_name)

class PlantSpecies(models.Model):
    common_name = models.CharField(max_length=100 , verbose_name="Nombre común" , unique = False)
    scientific_name =  models.CharField(max_length=100 , verbose_name="Nombre científico" , unique = True)
    family = models.ForeignKey(PlantFamily, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="familia" )
    description = models.TextField(blank=True,default="")
    photo = models.ImageField("Imagen", null=True, blank=True, upload_to="uploads/plant_family")


    #max_val = models.PositiveIntegerField(default=None, blank=True, null=True , verbose_name="Valor Máximo")
    #unit = models.CharField(max_length=20 , verbose_name="Unidad de medida" , blank = True , default = "")
    #order = models.PositiveIntegerField(default=0)
    #color = ColorField(default='#FF0000')


    class Meta:
        verbose_name = 'Especies de Plantas'
        verbose_name_plural = 'Especies de plantas'


    def __str__(self):
        return "%s" % (self.common_name)


class SpecimenStatus(models.Model):
    status_name = models.CharField(max_length=100 , verbose_name="Nombre" , unique = False)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return "%s" % (self.status_name)

class PlantSpecimen(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Perfil")
    photo = models.ImageField("Specimen Photo", null=False, blank=False, upload_to="uploads/specimen")
    date_received =  models.DateField("Fecha")
    status = models.ForeignKey(SpecimenStatus,on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Status")
    plant_family = models.ForeignKey(PlantFamily, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Family")
    plant_species = ChainedForeignKey(PlantSpecies , chained_field = "plant_family" , chained_model_field = "family", show_all=False , auto_choose=True, sort=True)

    class Meta:
        verbose_name = "Espécimen"
        verbose_name_plural = "Especimenes"

    def __str__(self):
        return "Espécimen de %s" % (self.plant_species.common_name)




#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)
#department = models.ForeignKey(Department, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="departamento")
#municipality = ChainedForeignKey(
#    Municipality,
#    chained_field="department",
#    chained_model_field="department",
#    show_all=False,
#    auto_choose=True,
#    sort=True)
