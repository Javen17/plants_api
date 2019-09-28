from .models import PlantSpecies ,  PlantFamily
from rest_framework import serializers



class PlantFamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantFamily
        fields = ['family_name']

class PlantSpeciesSerializer(serializers.HyperlinkedModelSerializer):

    family = PlantFamilySerializer()

    class Meta:
        model = PlantSpecies
        fields = ['common_name', 'scientific_name', 'family' , 'description' , 'photo']
