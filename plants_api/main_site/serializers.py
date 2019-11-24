from .models import Ecosystem, RecolectionAreaStatus , Biostatus , Status , Family, Genus, Species , Country , State , City  , Specimen, PlantSpecimen , MushroomSpecimen, CapType , FormType
from rest_framework import serializers
from plants_api.users.serializers import UserSerializer
from plants_api.users.models import User


class EcosystemSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Ecosystem.objects.all()).to_internal_value(data)

    class Meta:
        model = Ecosystem
        fields = '__all__'

class RecolectionAreaStatusSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=RecolectionAreaStatus.objects.all()).to_internal_value(data)

    class Meta:
        model = RecolectionAreaStatus
        fields = '__all__'

class BiostatusSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Biostatus.objects.all()).to_internal_value(data)

    class Meta:
        model = Biostatus
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Status.objects.all()).to_internal_value(data)

    class Meta:
        model = Status
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Family.objects.all()).to_internal_value(data)

    class Meta:
        model = Family
        fields = ['family_name']
        extra_kwargs = {
                'family_name': {'validators': []},
            }
        fields = '__all__'

class GenusSerializer(serializers.ModelSerializer):

    family = FamilySerializer()

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Genus.objects.all()).to_internal_value(data)

    class Meta:
        model = Genus
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Country.objects.all()).to_internal_value(data)

    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):

    country = CountrySerializer()

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=State.objects.all()).to_internal_value(data)

    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):

    state = StateSerializer()

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=City.objects.all()).to_internal_value(data)

    class Meta:
        model = City
        fields = '__all__'


class CapTypeSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=CapType.objects.all()).to_internal_value(data)

    class Meta:
        model = CapType
        fields = "__all__"

class FormTypeSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=FormType.objects.all()).to_internal_value(data)

    class Meta:
        model = FormType
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):

    family = FamilySerializer()
    genus = GenusSerializer()

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
    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField(queryset=Species.objects.all()).to_internal_value(data)


    class Meta:
        model = Species
        fields = '__all__'


#class SpecimenStatusSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = SpecimenStatus
#        fields = ['status_name']

class SpecimenSerializer():

    user =  UserSerializer()
    family = FamilySerializer()
    genus = GenusSerializer()
    species = SpeciesSerializer()
    status = StatusSerializer()
    ecosystem = EcosystemSerializer()
    recolection_area_status = RecolectionAreaStatusSerializer()

    country= CountrySerializer()
    state = StateSerializer()
    city = CitySerializer()


class PlantSpecimenSerializer(serializers.ModelSerializer , SpecimenSerializer):
    biostatus = BiostatusSerializer()
    class Meta:
        model = PlantSpecimen
        fields = "__all__"


class MushroomSpecimenSerializer(serializers.ModelSerializer , SpecimenSerializer):
    cap = CapTypeSerializer()
    forms = FormTypeSerializer()

    class Meta:
        model = MushroomSpecimen
        fields = "__all__"
