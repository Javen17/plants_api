from django.db import models
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import pre_save , post_save
from plants_api.users.models import User
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionRole, GoogleDrivePermissionType ,GoogleDriveFilePermission
from config import settings 
from plants_api.helpers import helpers 

# Create your models here.
permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.ANYONE
)

gd_storage = GoogleDriveStorage(permissions=(permission, ))

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

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'

    def __str__(self):
        return "%s" % (self.name)

class Species(models.Model):
    common_name = models.CharField(max_length=100 , verbose_name="Nombre común" , unique = False)
    scientific_name =  models.CharField(max_length=100 , verbose_name="Nombre científico" , unique = True)
    genus = models.ForeignKey(Genus , on_delete = models.CASCADE , verbose_name = "Género")
    description = models.TextField(blank=True,default="")
    photo = models.ImageField("Imagen" , upload_to="uploads/plant_family")

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

    def __init__(self, *args, **kwargs):
        super(Specimen, self).__init__(*args, **kwargs)
        self.original_approved = self.approved

    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="Usuario")
    photo = models.ImageField("Imagen" , upload_to="uploads/plant_family", storage=gd_storage)
    date_received =  models.DateTimeField("Fecha")
    species = models.ForeignKey(Species , on_delete = models.CASCADE, verbose_name = "Especie")
    status = models.ForeignKey(Status , on_delete=models.CASCADE , verbose_name = "Estado")
    number_of_samples = models.PositiveIntegerField("Número de ejemplares")
    description = models.TextField("Descripción" , blank=True , null=True)
    ecosystem = models.ForeignKey(Ecosystem , on_delete = models.CASCADE , verbose_name = "Ecosistema")
    recolection_area_status = models.ForeignKey(RecolectionAreaStatus , on_delete = models.CASCADE , verbose_name = "Estado del area de recolección")

    approved = models.BooleanField("Aprobado" , default = False , blank = True )

    city =  models.ForeignKey(City ,  on_delete = models.CASCADE  ,  verbose_name= "Ciudad/Municipio")

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


@receiver(post_save, sender=MushroomSpecimen)
@receiver(post_save, sender=PlantSpecimen)
def send_approved_message(sender, instance, **kwargs):
    if instance.original_approved != instance.approved:
        message_string = "Hola " + instance.user.name  + ". tu espécimen de " + instance.species.common_name + " registrado el " + instance.date_received.strftime("%d-%m-%Y") 
        if instance.approved:
            helpers.send_notification(instance.user.id, "Aprobación de ficha técnica" , message_string  + " ha sido aprobado")
        else:
            helpers.send_notification(instance.user.id, "Aprobación de ficha técnica" , message_string + " ha sido denegado")


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
