from django.shortcuts import render
from .models import PlantSpecies, PlantFamily
from rest_framework import viewsets
from .serializers import PlantSpeciesSerializer, PlantFamilySerializer
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
