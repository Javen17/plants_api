from django.contrib import admin
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status , Family , Genus , Species , Country , State , City,  PlantSpecimen ,MushroomSpecimen , FormType , CapType
from rest_framework.authtoken.models import Token

# Register your models here.
class SpeciesModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'scientific_name' , 'family')
    list_filter = ('family',)


admin.site.register(Ecosystem)
admin.site.register(RecolectionAreaStatus)
admin.site.register(Biostatus)
admin.site.register(Status)
admin.site.register(Family)
admin.site.register(Genus)
admin.site.register(Species , SpeciesModelAdmin)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(PlantSpecimen)
admin.site.register(FormType)
admin.site.register(CapType)
admin.site.register(MushroomSpecimen)
#admin.site.register(SpecimenStatus)
admin.site.unregister(Token)
