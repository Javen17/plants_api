from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from plants_api.users.models import User
# Create your models here.

TYPE_CHOICES = [
    ('planta', 'Planta'),
    ('hongo', 'Hongo'),
]

class Ecosystem(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre de hábitat")

    class Meta:
        verbose_name = 'Ecosistema'
        verbose_name_plural = 'Ecosistemas'

    def __str__(self):
        return "%s" % (self.name)


class RecolectionAreaStatus(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Descripción del habitad")

    class Meta:
        verbose_name = 'Descripción del habitad'
        verbose_name_plural = 'Descripciónes del habitad'

    def __str__(self):
        return "%s" % (self.name)


class Biostatus(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre de estado biológico")

    class Meta:
        verbose_name = 'Biostatus'
        verbose_name_plural = 'Biostatus'

    def __str__(self):
        return "%s" % (self.name)

class Status(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre del estado")

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return "%s" % (self.name)


class Family(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre de la familia" , unique = True)
    type =  models.CharField(max_length=100  , choices = TYPE_CHOICES , verbose_name = "Tipo")

    class Meta:
        verbose_name = 'Familias de plantas'
        verbose_name_plural = 'Familias de plantas'

    def __str__(self):
        return "%s" % (self.name)

class Genus(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre del Género" , unique = True)
    family = models.ForeignKey(Family , on_delete = models.CASCADE , verbose_name = "Familia")
    type =  models.CharField( max_length=100  , choices = TYPE_CHOICES , verbose_name = "Tipo")

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

    def __str__(self):
        return "%s" % (self.name)

class Species(models.Model):
    common_name = models.CharField(max_length=100 , verbose_name="Nombre común" , unique = False)
    scientific_name =  models.CharField(max_length=100 , verbose_name="Nombre científico" , unique = True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="familia" )
    genus = ChainedForeignKey(Genus , chained_field = "family" , chained_model_field = "family", show_all=False , auto_choose=True, sort=True)
    description = models.TextField(blank=True,default="")
    photo = models.ImageField("Imagen", null=True, blank=True, upload_to="uploads/plant_family")
    type =  models.CharField( max_length=100  , choices = TYPE_CHOICES , verbose_name = "Tipo")


    #max_val = models.PositiveIntegerField(default=None, blank=True, null=True , verbose_name="Valor Máximo")
    #unit = models.CharField(max_length=20 , verbose_name="Unidad de medida" , blank = True , default = "")
    #order = models.PositiveIntegerField(default=0)
    #color = ColorField(default='#FF0000')


    class Meta:
        verbose_name = 'Especies de Plantas'
        verbose_name_plural = 'Especies de plantas'


    def __str__(self):
        return "%s" % (self.common_name)


#class SpecimenStatus(models.Model):
#    status_name = models.CharField(max_length=100 , verbose_name="Nombre" , unique = False)
#
#    class Meta:
#        verbose_name = "Estado"
#        verbose_name_plural = "Estados"
#
#    def __str__(self):
#        return "%s" % (self.status_name)


class Country(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre")

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural = "Paises"

    def __str__(self):
        return "%s" % (self.name)


class State(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre")
    country = models.ForeignKey(Country , on_delete = models.CASCADE , verbose_name = "Pais")

    class Meta:
        verbose_name = "Estado/Departamentos/Provincias"
        verbose_name_plural = "Estados/Departamentos/Provincias"

    def __str__(self):
        return "%s" % (self.name)


class City(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre")
    state = models.ForeignKey(State , on_delete = models.CASCADE , verbose_name = "Estado")

    class Meta:
        verbose_name = "Ciudad/Municipio"
        verbose_name_plural = "Ciudades/Municipios"

    def __str__(self):
        return "%s" % (self.name)


class Specimen(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Usuario")
    photo = models.ImageField("Foto", null=True, blank=True , upload_to="uploads/specimen")
    date_received =  models.DateField("Fecha")
    family = models.ForeignKey(Family, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Family")
    genus = ChainedForeignKey(Genus , chained_field = "family" , chained_model_field = "family", on_delete=models.CASCADE , blank = False , default = 0 , verbose_name = "Género")
    species = ChainedForeignKey(Species , chained_field = "genus" , chained_model_field = "genus", show_all=False , auto_choose=True, sort=True)
    status = models.ForeignKey(Status , on_delete=models.CASCADE , verbose_name = "Estado")
    number_of_samples = models.PositiveIntegerField("Número de ejemplares")
    description = models.TextField("Descripción" , blank=True , null=True)
    ecosystem = models.ForeignKey(Ecosystem , on_delete = models.CASCADE , verbose_name = "Ecosistema")
    recolection_area_status = models.ForeignKey(RecolectionAreaStatus , on_delete = models.CASCADE , verbose_name = "Estado del area de recolección")

    approved = models.BooleanField("Aprobado" , default = False , blank = True )

    country = models.ForeignKey(Country , on_delete=models.CASCADE , blank = False , verbose_name = "País")
    state = ChainedForeignKey(State , chained_field = "country" , chained_model_field = "country" , verbose_name= "Estado/Departamento/Provincia")
    city =  ChainedForeignKey(City , chained_field = "state" , chained_model_field = "state" ,   verbose_name= "Ciudad/Municipio")

    latitude  = models.FloatField("Latitud" , blank=True , null=True)
    longitude =  models.FloatField("Longitud" , blank=True , null=True)

    location = models.CharField(max_length=100 , verbose_name="Ubicación")

    class Meta:
        abstract = True

class PlantSpecimen(Specimen):
    biostatus = models.ForeignKey(Biostatus , on_delete = models.CASCADE , verbose_name = "Biostatus")
    complete  = models.BooleanField("Completo")

    class Meta:
        verbose_name = "Espécimen de planta"
        verbose_name_plural = "Especimenes de plantas"

    def __str__(self):
        return "Espécimen de %s" % (self.species.common_name)


class CapType(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre")

    class Meta:
        verbose_name = "Tipo de sombrero de hongo"
        verbose_name_plural = "Tipos de sombrero de hongo"

    def __str__(self):
        return "%s" % (self.name)


class FormType(models.Model):
    name = models.CharField(max_length=100 , verbose_name="Nombre")

    class Meta:
        verbose_name = "Tipo de forma de hongo"
        verbose_name_plural = "Tipos de forma de hongos"

    def __str__(self):
        return "%s" % (self.name)

class MushroomSpecimen(Specimen):
    cap = models.ForeignKey( CapType , verbose_name="Forma de sombrero" , on_delete=models.CASCADE)
    forms = models.ForeignKey(FormType ,  verbose_name = "Forma de hongo" , on_delete=models.CASCADE)
    crust = models.BooleanField("¿Tiene costra?")
    color = models.CharField(max_length = 100 , verbose_name = "color")
    change_of_color = models.CharField(max_length = 100 , verbose_name = "Cambios de color")
    smell = models.CharField(max_length = 100 , verbose_name = "olor")
    aditional_info = models.TextField("Información Adicional", blank=True , null=True)

    class Meta:
        verbose_name = "Espécimen de hongo"
        verbose_name_plural = "Especimenes de hongos"

    def __str__(self):
        return "Espécimen de %s" % (self.species.common_name)

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
