from django.shortcuts import render
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status ,  Species, Family , Genus , Country , State ,  City , CapType , FormType , PlantSpecimen , MushroomSpecimen
from plants_api.users.models import User
from plants_api.users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import EcosystemSerializer, RecolectionAreaStatusSerializer , BiostatusSerializer , StatusSerializer , SpeciesSerializer, FamilySerializer , GenusSerializer , CountrySerializer, StateSerializer , CitySerializer , CapTypesSerializer , FormTypeSerializer , PlantSpecimenSerializer , MushroomSpecimenSerializer
from django.http import HttpResponse , JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from rest_framework import permissions
from plants_api.helpers import helpers

#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView

class EcosystemViewSet(viewsets.ModelViewSet):
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class RecolectionAreaStatusViewSet(viewsets.ModelViewSet):
    queryset = RecolectionAreaStatus.objects.all()
    serializer_class = RecolectionAreaStatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class BiostatusViewSet(viewsets.ModelViewSet):
    queryset = Biostatus.objects.all()
    serializer_class = BiostatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.DjangoModelPermissions]

class GenusViewSet(viewsets.ModelViewSet):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.DjangoModelPermissions]


class CapTypeViewSet(viewsets.ModelViewSet):
    queryset = CapType.objects.all()
    serializer_class = CapTypesSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class FormTypeViewSet(viewsets.ModelViewSet):
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class SpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = SpeciesSerializer
    queryset = Species.objects.all()
    parser_class = (FileUploadParser,)

    permission_classes = [permissions.DjangoModelPermissions]

#    def perform_create(self, serializer):
#
#        if serializer.is_valid():
#
#            family_data = serializer.validated_data['family']
#            family_name = family_data["family_name"]
#
#            if family_name != '':
#
#                #family = get_or_created_family(family_data)
#                family = get_or_create_model_instance(["family_name"] , [family_name] , PlantFamily , PlantFamily() , "family_name" , family_name)
#

#                model_instance = PlantSpecies(common_name = serializer.validated_data.get("common_name") ,
#                    scientific_name = serializer.validated_data.get("scientific_name"),
#                    description = serializer.validated_data.get("description"),
#                    photo = serializer.validated_data.get("photo"),
#                    family = family)

#                model_instance.save()

#                return JsonResponse({"message": "success"})
#            else:
#                return JsonResponse(data={'message': 'Empty product_name'}, status=status.HTTP_400_BAD_REQUEST)
#        else:
#            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"] , detail = False)
    def search_species(self , request , pk = None):
        common_name = self.request.query_params.get('common_name',None)
        result = helpers.search(self.queryset , "common_name__icontains" , common_name , SpeciesSerializer)

        json = JSONRenderer().render(result)
        return HttpResponse(json)


#class SpecimenStatusViewSet(viewsets.ModelViewSet):
#    serializer_class = SpecimenStatusSerializer
#    queryset = SpecimenStatus


class PlantSpecimenViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]

    #def perform_create(self,serializer):
#
#        if serializer.is_valid():
#
#            family_data = serializer.validated_data["plant_family"]
#            family_name = family_data["family_name"]
#
#            user_data = serializer.validated_data["user"]
#            user_name = profile_data["username"]

#            species_data = serializer.validated_data["plant_species"]
#            status_data = serializer.validated_data["status"]

#            if family_name != "" and user_name != "" and species_data != "" and status_data != "":

#                user = get_or_create_model_instance(["name" , "photo"] , [user_name , user_data["profile_photo"]] , Profile , Profile() , "name" , profile_name)
#                family = get_or_create_model_instance(["family_name"] , [family_name] , PlantFamily , PlantFamily() , "family_name" , family_name)
#                species = get_or_create_model_instance(["common_name","scientific_name","family","description","photo"] , [species_data["common_name"] , species_data["scientific_name"] ,  family , species_data["description"] , species_data["photo"]] , PlantSpecies , PlantSpecies() , "scientific_name" , species_data["scientific_name"] )
#                status = get_or_create_model_instance(["status_name"] , [status_data["status_name"]] , SpecimenStatus , SpecimenStatus() , "status_name" , status_data["status_name"])

#                model_instance = PlantSpecimen( received_by =  profile ,
#                    photo = serializer.validated_data.get("photo") ,
#                    date_received = serializer.validated_data.get("date_received"),
#                    status = status ,
#                    plant_family = family,
#                    plant_species = species)

#                model_instance.save()

#                return JsonResponse({"message": "success"})
#            else:
#                return JsonResponse(data={'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
#        else:
#            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def search_specimen(self, request, pk=None):
        plant_species = self.request.query_params.get('species', None)
        result = helpers.search(self.queryset , "species__common_name__icontains" , species , SpecimenSerializer)
        json = JSONRenderer().render(result)
        return HttpResponse(json)


class MushroomSpecimenViewSet(viewsets.ModelViewSet):
    queryset = MushroomSpecimen.objects.all()
    serializer_class = MushroomSpecimenSerializer
    permission_classes = [permissions.DjangoModelPermissions]
