from django.shortcuts import render
from .models import PlantSpecies, PlantFamily , PlantSpecimen , SpecimenStatus , Recolector
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PlantSpeciesSerializer, PlantFamilySerializer , PlantSpecimenSerializer , SpecimenStatusSerializer , RecolectorSerializer
from django.http import HttpResponse , JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
class PlantFamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PlantFamily.objects.all()
    serializer_class = PlantFamilySerializer

class PlantSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpeciesSerializer
    queryset = PlantSpecies.objects.all()

    def perform_create(self, serializer):

        if serializer.is_valid():

            family_data = serializer.validated_data['family']
            family_name = family_data["family_name"]

            if family_name != '':
                family_list = PlantFamily.objects.filter(
                    family_name=family_name)

                if not family_list:
                    new_family = PlantFamily(family_name = family_name)
                    family = new_family
                    new_family.save()
                else:
                    family = family_list[0]

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

class RecolectorViewSet(viewsets.ModelViewSet):
    serializer_class = RecolectorSerializer
    queryset = Recolector.objects.all()

    @action(methods=['get'], detail=False)
    def search_recolector(self, request, pk=None):
        name = self.request.query_params.get('name', None)
        result = search(self.queryset , "name__icontains" , name)

        print(result)

        json = JSONRenderer().render(result)
        return HttpResponse(json)


class SpecimenStatusViewSet(viewsets.ModelViewSet):
    serializer_class = SpecimenStatusSerializer
    queryset = SpecimenStatus

class PlantSpecimenViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all()



def search(queryset , filter ,  search_field):

    if search_field is not None:
        q_objects = Q()
        q_objects = Q(**{ filter : search_field })

        found_elements = queryset.filter(q_objects)
        resultdict = {}

        for found in found_elements:
            serializer = RecolectorSerializer(found)
            resultdict.update(serializer.data)

        return resultdict
    else:
        return  "please provide a valid search url"
