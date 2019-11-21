from .models import Ecosystem, RecolectionAreaStatus , Biostatus , Status , Family, Genus, Species , Country , State , City  , Specimen, PlantSpecimen , MushroomSpecimen, CapType , FormType
from rest_framework import serializers
from plants_api.users.serializers import UserSerializer
from plants_api.users.models import User


class EcosystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecosystem
        fields = '__all__'

class RecolectionAreaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecolectionAreaStatus
        fields = '__all__'

class BiostatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biostatus
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['family_name']
        extra_kwargs = {
                'family_name': {'validators': []},
            }
        fields = '__all__'

class GenusSerializer(serializers.ModelSerializer):

    family = serializers.PrimaryKeyRelatedField(queryset= Family.objects.all())

    class Meta:
        model = Genus
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):

    Country = serializers.PrimaryKeyRelatedField(queryset= Country.objects.all())

    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):

    State = serializers.PrimaryKeyRelatedField(queryset= State.objects.all())

    class Meta:
        model = City
        fields = '__all__'


class CapTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapType

class FormTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormType
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):

    family = serializers.PrimaryKeyRelatedField(queryset= Family.objects.all())
    genus = serializers.PrimaryKeyRelatedField(queryset= Genus.objects.all())

    #def create(self, validated_data):

    #    family = validated_data.get("family")

    #    print("hola")

    #    try:
    #        family = PlantFamily.objects.get(family_name=family["family_name"]).first()
    #    except:
    #        family = validated_data.get("family")
    #        new_family = PlantFamily(family_name = family["family_name"])
    #        new_family.save()
    #        family = new_family

    #    species = PlantSpecies(
    #    common_name= validated_data.get("common_name") ,
    #    scientific_name = validated_data.get("scientific_name"),
    #    description = validated_data.get("description"),
    #    photo = validated_data.get("photo"),
    #    family = family
    #    )

    #    species.save()
    #    return validated_data

    class Meta:
        model = Species
        fields = '__all__'


#class SpecimenStatusSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = SpecimenStatus
#        fields = ['status_name']

class SpecimenSerializer():

    user =  serializers.PrimaryKeyRelatedField(queryset= User.objects.all())
    family = serializers.PrimaryKeyRelatedField(queryset= Family.objects.all())
    genus = serializers.PrimaryKeyRelatedField(queryset= Genus.objects.all())
    species = serializers.PrimaryKeyRelatedField(queryset= Species.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset= Status.objects.all())
    ecosystem = serializers.PrimaryKeyRelatedField(queryset= Ecosystem.objects.all())
    recolection_area_status = serializers.PrimaryKeyRelatedField(queryset= RecolectionAreaStatus)

    country= serializers.PrimaryKeyRelatedField(queryset= Country)
    state = serializers.PrimaryKeyRelatedField(queryset= State)
    city = serializers.PrimaryKeyRelatedField(queryset= City)


class PlantSpecimenSerializer(SpecimenSerializer , serializers.ModelSerializer):
    biostatus = serializers.PrimaryKeyRelatedField(queryset= Biostatus.objects.all())

    class Meta:
        model = PlantSpecimen
        fields = "__all__"

class MushroomSpecimenSerializer(SpeciesSerializer , serializers.ModelSerializer):
    cap = serializers.PrimaryKeyRelatedField(queryset= CapType.objects.all())
    forms = serializers.PrimaryKeyRelatedField(queryset= FormType.objects.all())

    class Meta:
        model = MushroomSpecimen
        fields = "__all__"
