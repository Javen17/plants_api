from django.shortcuts import render
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status ,  Species, Family , Genus , Country , State ,  City , CapType , FormType , PlantSpecimen , MushroomSpecimen
from plants_api.users.models import User
from plants_api.users.views import UserViewSet
from plants_api.users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import EcosystemSerializer, RecolectionAreaStatusSerializer , BiostatusSerializer , StatusSerializer , SpeciesSerializer , SpeciesExcludeSerializer , FamilySerializer , GenusSerializer , CountrySerializer, StateSerializer , CitySerializer , CapTypeSerializer , FormTypeSerializer , PlantSpecimenSerializer ,PlantSpecimenExcludeSerializer , MushroomSpecimenSerializer , MushroomSpecimenExcludeSerializer
from django.http import HttpResponse , JsonResponse , StreamingHttpResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from rest_framework import permissions
from plants_api.helpers import helpers
from urllib.parse import parse_qs
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from plants_api.common.base_classes import BaseGoogleFixClass , SearchAndPatchMixin
from docx import Document
#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView

class EcosystemViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class RecolectionAreaStatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = RecolectionAreaStatus.objects.all()
    serializer_class = RecolectionAreaStatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class BiostatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Biostatus.objects.all()
    serializer_class = BiostatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class StatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class FamilyViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.DjangoModelPermissions]

class GenusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class CountryViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.DjangoModelPermissions]

class StateViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class CityViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.DjangoModelPermissions]

class CapTypeViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = CapType.objects.all()
    serializer_class = CapTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class FormTypeViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class SpeciesViewSet(BaseGoogleFixClass , SearchAndPatchMixin, viewsets.ModelViewSet):
    serializer_class = SpeciesSerializer
    queryset = Species.objects.all()
    parser_class = (FileUploadParser,)
    exclude_serializer = SpeciesExcludeSerializer
    permission_classes = [permissions.DjangoModelPermissions]


#this two classes should be one
class PlantSpecimenViewSet(BaseGoogleFixClass , viewsets.ModelViewSet , SearchAndPatchMixin):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all().select_related( 'user' , 'species', 'status', 'ecosystem', 'recolection_area_status' , 'city' , 'biostatus') 
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head' , 'put' , 'patch']
    model = PlantSpecimen
    exclude_serializer = PlantSpecimenExcludeSerializer

    def get_permissions(self):
        if self.action in ["list" , "retrieve" , "search", "filter" , "approved"]:
            return [permissions.AllowAny(), ]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.has_perm("view_plantspecimen"):
            return self.queryset
        else:
            return self.queryset.filter(approved = True)

    def update(self, request, partial  = False , pk = None):
        
        if pk is not None:
            approved = request.data.get("approved")

            if (request.user.has_perm("change_plant_approval") and approved) or  approved is None:
                return self.edit(request , pk , partial)
            else:
                return JsonResponse({"result" : "Bad Request"} , status = 400)
        else:
            return JsonResponse({"result" : "Bad Request"} , status = 400)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get'] , detail=False)
    def approved(self, request , pk=None):
        result =  self.exclude_serializer(self.queryset.filter(approved=True), many = True).data
        return JsonResponse(result, safe=False)     
    
    @action(methods=['get'], detail=True)
    def report(self, request, pk):
        specimen = self.get_queryset().filter(pk = pk).first()
        document = helpers.build_report(specimen)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Ficha-{}.docx"'.format(specimen.species.common_name)
        document.save(response)
        return response
    
class MushroomSpecimenViewSet(BaseGoogleFixClass , SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = MushroomSpecimen.objects.all().select_related( 'user' , 'species', 'status', 'ecosystem', 'recolection_area_status' , 'city' , 'cap' , 'forms') 
    serializer_class = MushroomSpecimenSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head' , 'put' , 'patch']
    model = MushroomSpecimen
    exclude_serializer = MushroomSpecimenExcludeSerializer

    def get_permissions(self):
        if self.action in ["list" , "retrieve" , "search", "filter" , "approved"]:
            return [permissions.AllowAny(), ]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.has_perm("view_mushroomspecimen"):
            return self.queryset
        else:
            return self.queryset.filter(approved = True)
   
    def update(self , request, partial  = False , pk = None):
        if pk is not None:
            approved = request.data.get("approved")

            if (request.user.has_perm("change_mushroom_approval") and approved) or  approved is None:
                return self.edit(request , pk , partial)
            else:
                return JsonResponse({"result" : "Bad Request"} , status = 400)
        else:
            return JsonResponse({"result" : "Bad Request"} , status = 400)
                
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get'], detail=True)
    def report(self, request, pk):
        specimen = self.get_queryset().filter(pk = pk).first()
        document = helpers.build_report(specimen)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Ficha-{}.docx"'.format(specimen.species.common_name)
        document.save(response)
        return response

class StatsView(APIView):

    def get(self , request):
        user= len(User.objects.all())
        plants = len(PlantSpecimen.objects.all())
        mushroom = len(MushroomSpecimen.objects.all())

        result = {
            "user_number" : user ,
            "plant_number" : plants,
            "mushroom_number" :  mushroom
        }

        return JsonResponse({"result": result})

#class NotificationDemoView(APIView):

#    def get(self , request):
#        helpers.send_notification( "This is a enriched message" , "egAn5eu7EA8:APA91bFc0sbm3hXXBvDJB6mSdQBiSjH0gtcm5mUvKC3R0EsKMLAHesv6fCyoUoah5ygnTT0Ib4TU6yvZbKmTrPu1vDh0mTBUzozQMeDVTQfu0he5fsdxnjkCdQffaJjiDwUP6dh94qHS")
#        return JsonResponse({"result": "prueba"})


