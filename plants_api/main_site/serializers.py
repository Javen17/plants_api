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
        fields = '__all__'

class GenusSerializer(serializers.ModelSerializer):

    family = FamilySerializer()

    def to_internal_value(self, data):
        self.fields['family'] = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
        return super(GenusSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['family'] = FamilySerializer()
        return super(GenusSerializer, self).to_representation(obj)

    class Meta:
        model = Genus
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):

    country = CountrySerializer()

    def to_internal_value(self, data):
        self.fields['country'] = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
        return super(StateSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['country'] = CountrySerializer()
        return super(StateSerializer, self).to_representation(obj)

    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):

    state = StateSerializer()

    def to_internal_value(self, data):
        self.fields['state'] = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
        return super(CitySerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['state'] = StateSerializer()
        return super(CitySerializer, self).to_representation(obj)

    class Meta:
        model = City
        fields = '__all__'


class CapTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CapType
        fields = "__all__"

class FormTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormType
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):

    genus = GenusSerializer()

    def to_internal_value(self, data):
        self.fields['genus'] = serializers.PrimaryKeyRelatedField(queryset=Genus.objects.all())
        return super(SpeciesSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['genus'] = GenusSerializer()
        return super(SpeciesSerializer, self).to_representation(obj)


    class Meta:
        model = Species
        fields = '__all__'

class SpeciesExcludeSerializer(SpeciesSerializer): 

    class Meta:
        model = Species
        exclude = ('photo', )

#class SpecimenStatusSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = SpecimenStatus
#        fields = ['status_name']

class SpecimenSerializer():

    user =  UserSerializer()
    species = SpeciesSerializer()
    status = StatusSerializer()
    ecosystem = EcosystemSerializer()
    recolection_area_status = RecolectionAreaStatusSerializer()

    city = CitySerializer()

    def to_internal_value(self, data):
        self.fields['user'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        self.fields['species'] = serializers.PrimaryKeyRelatedField(queryset=Species.objects.all())
        self.fields['status'] = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
        self.fields['ecosystem'] = serializers.PrimaryKeyRelatedField(queryset=Ecosystem.objects.all())
        self.fields['recolection_area_status'] = serializers.PrimaryKeyRelatedField(queryset=RecolectionAreaStatus.objects.all())

        self.fields['city'] = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

        return super(SpecimenSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['user'] = UserSerializer()
        self.fields['status'] = StatusSerializer()
        self.fields['ecosystem'] = EcosystemSerializer()
        self.fields['recolection_area_status'] = RecolectionAreaStatusSerializer()
        self.fields['city'] = CitySerializer()
        return super(SpecimenSerializer, self).to_representation(obj)


class PlantSpecimenSerializer(SpecimenSerializer , serializers.ModelSerializer):
    biostatus = BiostatusSerializer()

    def to_internal_value(self, data):
        self.fields['biostatus'] = serializers.PrimaryKeyRelatedField(queryset=Biostatus.objects.all())
        return super(PlantSpecimenSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['species'] = SpeciesSerializer()
        self.fields['biostatus'] = BiostatusSerializer()
        return super(PlantSpecimenSerializer, self).to_representation(obj)

    class Meta:
        model = PlantSpecimen
        fields = "__all__"


class PlantSpecimenExcludeSerializer(PlantSpecimenSerializer): 
    species = SpeciesExcludeSerializer()

    def to_representation(self, obj):
        self.fields['species'] = SpeciesExcludeSerializer()
        self.fields['biostatus'] = BiostatusSerializer()
        return super(PlantSpecimenSerializer, self).to_representation(obj)

    class Meta:
        model = PlantSpecimen
        exclude = ('photo', )


class MushroomSpecimenSerializer(SpecimenSerializer , serializers.ModelSerializer):
    cap = CapTypeSerializer()
    forms = FormTypeSerializer()

    def to_internal_value(self, data):
        self.fields['cap'] = serializers.PrimaryKeyRelatedField(queryset=CapType.objects.all())
        self.fields['forms'] = serializers.PrimaryKeyRelatedField(queryset=FormType.objects.all())
        return super(MushroomSpecimenSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['cap'] = CapTypeSerializer()
        self.fields['forms'] = FormTypeSerializer()
        return super(MushroomSpecimenSerializer, self).to_representation(obj)

    class Meta:
        model = MushroomSpecimen
        fields = "__all__"

class MushroomSpecimenExcludeSerializer(MushroomSpecimenSerializer): 
    species = SpeciesExcludeSerializer()

    def to_representation(self, obj):
        self.fields['species'] = SpeciesExcludeSerializer()
        self.fields['cap'] = CapTypeSerializer()
        self.fields['forms'] = FormTypeSerializer()
        return super(MushroomSpecimenSerializer, self).to_representation(obj)

    class Meta:
        model = MushroomSpecimen
        exclude = ('photo', )