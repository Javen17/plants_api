from django.db import models
from smart_selects.db_fields import ChainedForeignKey

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




#department = models.ForeignKey(Department, on_delete=models.CASCADE , blank = False , default =0 ,  verbose_name="departamento")
#municipality = ChainedForeignKey(
#    Municipality,
#    chained_field="department",
#    chained_model_field="department",
#    show_all=False,
#    auto_choose=True,
#    sort=True)
