from django.contrib import admin
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status , Family , Genus , Species , Country , State , City,  PlantSpecimen ,MushroomSpecimen , FormType , CapType
from rest_framework.authtoken.models import Token

# Register your models here.
class SpeciesModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'scientific_name' ,  'genus')
    list_filter = ('genus',)

@admin.register(PlantSpecimen)
class PlantSpecimenModelAdmin(admin.ModelAdmin):
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser and not request.user.has_perm("change_plant_approval"):
            disabled_fields |= {
                'approved',
             }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

@admin.register(MushroomSpecimen)
class MushroomSpecimenModelAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser and not request.user.has_perm("change_mushroom_approval"):
            form.fields['approved'].disabled = True

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


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
admin.site.register(FormType)
admin.site.register(CapType)
#admin.site.register(SpecimenStatus)
admin.site.unregister(Token)
