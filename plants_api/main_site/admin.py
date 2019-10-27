from django.contrib import admin
from .models import PlantFamily , PlantSpecies , SpecimenStatus , PlantSpecimen

# Register your models here.
class PlantSpeciesModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'scientific_name' , 'family')
    list_filter = ('family',)



admin.site.register(PlantFamily)
admin.site.register(PlantSpecies , PlantSpeciesModelAdmin)
admin.site.register(PlantSpecimen)
admin.site.register(SpecimenStatus)
