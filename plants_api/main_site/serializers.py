from .models import PlantSpecies ,  PlantFamily , Recolector , PlantSpecimen , SpecimenStatus
from rest_framework import serializers



class PlantFamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantFamily
        fields = ['family_name']
        extra_kwargs = {
                'family_name': {'validators': []},
            }

class PlantSpeciesSerializer(serializers.HyperlinkedModelSerializer):

    family = PlantFamilySerializer()

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
        fields = ['common_name', 'scientific_name', 'family' , 'description' , 'photo']


class RecolectorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Recolector
        fields = ['name' , 'photo']


class SpecimenStatusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SpecimenStatus
        fields = ['status_name']

class PlantSpecimenSerializer(serializers.HyperlinkedModelSerializer):

    recolector = RecolectorSerializer()
    plant_family = PlantFamilySerializer()
    plant_species = PlantSpeciesSerializer()
    status = SpecimenStatusSerializer()

    class Meta:
        model = PlantSpecimen
        fields = ['recolector', 'photo', 'date_received' , 'status' , 'plant_family' , 'plant_species']
