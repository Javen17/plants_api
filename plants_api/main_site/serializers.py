from .models import PlantSpecies ,  PlantFamily , PlantSpecimen , SpecimenStatus
from rest_framework import serializers
from plants_api.users.serializers import UserSerializer
from plants_api.users.models import User


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = ['family_name']
        extra_kwargs = {
                'family_name': {'validators': []},
            }
        fields = '__all__'

class PlantSpeciesSerializer(serializers.ModelSerializer):

    family = serializers.PrimaryKeyRelatedField(queryset= PlantFamily.objects.all())


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
        model = PlantSpecies
        fields = '__all__'


class SpecimenStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecimenStatus
        fields = ['status_name']

class PlantSpecimenSerializer(serializers.ModelSerializer):

    user =  serializers.PrimaryKeyRelatedField(queryset= User.objects.all())
    plant_family = serializers.PrimaryKeyRelatedField(queryset= PlantFamily.objects.all())
    plant_species = serializers.PrimaryKeyRelatedField(queryset= PlantSpecimen.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset= SpecimenStatus.objects.all())

    class Meta:
        model = PlantSpecimen
        fields = '__all__'
