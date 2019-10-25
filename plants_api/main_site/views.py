from django.shortcuts import render
from .models import PlantSpecies, PlantFamily , PlantSpecimen , SpecimenStatus , Recolector
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PlantSpeciesSerializer, PlantFamilySerializer , PlantSpecimenSerializer , SpecimenStatusSerializer , RecolectorSerializer
from django.http import HttpResponse , JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from rest_framework import permissions

#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
class PlantFamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PlantFamily.objects.all()
    serializer_class = PlantFamilySerializer
    permission_classes = [permissions.IsAuthenticated]

class PlantSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpeciesSerializer
    queryset = PlantSpecies.objects.all()
    parser_class = (FileUploadParser,)

    def perform_create(self, serializer):

        if serializer.is_valid():

            family_data = serializer.validated_data['family']
            family_name = family_data["family_name"]

            if family_name != '':

                #family = get_or_created_family(family_data)
                family = get_or_create_model_instance(["family_name"] , [family_name] , PlantFamily , PlantFamily() , "family_name" , family_name)


                model_instance = PlantSpecies(common_name = serializer.validated_data.get("common_name") ,
                    scientific_name = serializer.validated_data.get("scientific_name"),
                    description = serializer.validated_data.get("description"),
                    photo = serializer.validated_data.get("photo"),
                    family = family)

                model_instance.save()

                return JsonResponse({"message": "success"})
            else:
                return JsonResponse(data={'message': 'Empty product_name'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"] , detail = False)
    def search_species(self , request , pk = None):
        common_name = self.request.query_params.get('common_name',None)
        result = search(self.queryset , "common_name__icontains" , common_name , PlantSpeciesSerializer)

        json = JSONRenderer().render(result)
        return HttpResponse(json)


class RecolectorViewSet(viewsets.ModelViewSet):
    serializer_class = RecolectorSerializer
    queryset = Recolector.objects.all()

    @action(methods=['get'], detail=False)
    def search_recolector(self, request, pk=None):
        name = self.request.query_params.get('name', None)
        result = search(self.queryset , "name__icontains" , name , RecolectorSerializer )

        json = JSONRenderer().render(result)
        return HttpResponse(json)


class SpecimenStatusViewSet(viewsets.ModelViewSet):
    serializer_class = SpecimenStatusSerializer
    queryset = SpecimenStatus


class PlantSpecimenViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all()

    def perform_create(self,serializer):

        if serializer.is_valid():

            family_data = serializer.validated_data["plant_family"]
            family_name = family_data["family_name"]

            recolector_data = serializer.validated_data["recolector"]
            recolector_name = recolector_data["name"]

            species_data = serializer.validated_data["plant_species"]
            status_data = serializer.validated_data["status"]

            if family_name != "" and recolector_name != "" and species_data != "" and status_data != "":

                recolector = get_or_create_model_instance(["name" , "photo"] , [recolector_name , recolector_data["photo"]] , Recolector , Recolector() , "name" , recolector_name)
                family = get_or_create_model_instance(["family_name"] , [family_name] , PlantFamily , PlantFamily() , "family_name" , family_name)
                species = get_or_create_model_instance(["common_name","scientific_name","family","description","photo"] , [species_data["common_name"] , species_data["scientific_name"] ,  family , species_data["description"] , species_data["photo"]] , PlantSpecies , PlantSpecies() , "scientific_name" , species_data["scientific_name"] )
                status = get_or_create_model_instance(["status_name"] , [status_data["status_name"]] , SpecimenStatus , SpecimenStatus() , "status_name" , status_data["status_name"])

                model_instance = PlantSpecimen( recolector = recolector ,
                    photo = serializer.validated_data.get("photo") ,
                    date_received = serializer.validated_data.get("date_received"),
                    status = status ,
                    plant_family = family,
                    plant_species = species)

                model_instance.save()

                return JsonResponse({"message": "success"})
            else:
                return JsonResponse(data={'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def search_specimen(self, request, pk=None):
        plant_species = self.request.query_params.get('plant_species', None)
        result = search(self.queryset , "plant_species__common_name__icontains" , plant_species , PlantSpecimenSerializer)
        json = JSONRenderer().render(result)
        return HttpResponse(json)


def search(queryset , filter ,  search_field , serializer):

    if search_field is not None:
        q_objects = Q()
        q_objects = Q(**{ filter : search_field })

        found_elements = queryset.filter(q_objects)
        resultdict = {}

        for found in found_elements:
            serializer = serializer(found)
            resultdict.update(serializer.data)

        return resultdict
    else:
        return  "please provide a valid search url"


def get_or_create_model_instance(arguments_list , arguments_values , model_manager , model , search_field , value):

    model_list = model_manager.objects.filter(**{search_field: value})

    if not model_list:
        i = 0
        for argument_l in arguments_list:
            setattr(model, argument_l , arguments_values[i])
            i += 1
            try:
                model.save()
            except ValueError as err:
                return {"message" : err.args}
    else:
        model = model_list[0]

    return model
