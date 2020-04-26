from django.shortcuts import render
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status ,  Species, Family , Genus , Country , State ,  City , CapType , FormType , PlantSpecimen , MushroomSpecimen
from plants_api.users.models import User
from plants_api.users.views import UserViewSet
from plants_api.users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import EcosystemSerializer, RecolectionAreaStatusSerializer , BiostatusSerializer , StatusSerializer , SpeciesSerializer , SpeciesExcludeSerializer , FamilySerializer , GenusSerializer , CountrySerializer, StateSerializer , CitySerializer , CapTypeSerializer , FormTypeSerializer , PlantSpecimenSerializer ,PlantSpecimenExcludeSerializer , MushroomSpecimenSerializer , MushroomSpecimenExcludeSerializer
from django.http import HttpResponse , JsonResponse
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
#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView

class EcosystemViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(EcosystemViewSet, self).get_permissions()


class RecolectionAreaStatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = RecolectionAreaStatus.objects.all()
    serializer_class = RecolectionAreaStatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(RecolectionAreaStatusViewSet, self).get_permissions()

class BiostatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Biostatus.objects.all()
    serializer_class = BiostatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(BiostatusViewSet, self).get_permissions()


class StatusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(StatusViewSet, self).get_permissions()


class FamilyViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(FamilyViewSet, self).get_permissions()

class GenusViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(GenusViewSet, self).get_permissions()


class CountryViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CountryViewSet, self).get_permissions()


class StateViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(StateViewSet, self).get_permissions()


class CityViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CityViewSet, self).get_permissions()

class CapTypeViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = CapType.objects.all()
    serializer_class = CapTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CapTypeViewSet, self).get_permissions()


class FormTypeViewSet(SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(FormTypeViewSet, self).get_permissions()

class SpeciesViewSet(BaseGoogleFixClass , SearchAndPatchMixin, viewsets.ModelViewSet):
    serializer_class = SpeciesSerializer
    queryset = Species.objects.all()
    parser_class = (FileUploadParser,)
    exclude_serializer = SpeciesExcludeSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get_permissions(self):
        if self.action in ["list" , "retrieve" , "search", "filter"]:
            return [permissions.AllowAny(), ]
        return super(SpeciesViewSet, self).get_permissions()


class PlantSpecimenViewSet(BaseGoogleFixClass , SearchAndPatchMixin  , viewsets.ModelViewSet):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all().select_related( 'user' , 'species', 'status', 'ecosystem', 'recolection_area_status' , 'city' , 'biostatus') 
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head' , 'put' , 'patch']
    model = PlantSpecimen
    exclude_serializer = PlantSpecimenExcludeSerializer

    def update(self, request, partial  = False , pk = None):

        if pk is not None:
            approved = request.data.get("approved")

            if (request.user.has_perm("change_plant_approval") and approved) or  approved is None:
                return self.edit(request , pk , partial)
            else:
                return JsonResponse({"result" : "Bad Request"} , status = 400)
        else:
            return JsonResponse({"result" : "Bad Request"} , status = 400)

    def retrieve(self, request, pk=None):
        if request.user.has_perm("view_plantspecimen"):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(approved = True)
        
        plant = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(plant)
        return JsonResponse(serializer.data)

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "approved":
            return [permissions.AllowAny(), ]
        return super(PlantSpecimenViewSet, self).get_permissions()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])

        if request.user.has_perm("view_plantspecimen"):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(approved = True)

        result = helpers.search(queryset , params , PlantSpecimenSerializer , "OR")
        return JsonResponse(result, safe=False)

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , PlantSpecimenSerializer , "AND")

        return JsonResponse(result, safe=False)

    @action(methods=['get'] , detail=False)
    def approved(self, request , pk=None):
        result =  self.serializer_class(self.queryset.filter(approved=True), many = True).data
        return JsonResponse(result, safe=False)     
    

class MushroomSpecimenViewSet(BaseGoogleFixClass , SearchAndPatchMixin , viewsets.ModelViewSet):
    queryset = MushroomSpecimen.objects.all().select_related( 'user' , 'species', 'status', 'ecosystem', 'recolection_area_status' , 'city' , 'cap' , 'forms') 
    serializer_class = MushroomSpecimenSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head' , 'put' , 'patch']
    model = MushroomSpecimen
    exclude_serializer = MushroomSpecimenExcludeSerializer

    def update(self , request, partial  = False , pk = None):

        if pk is not None:
            approved = request.data.get("approved")

            if (request.user.has_perm("change_mushroom_approval") and approved) or  approved is None:
                return self.edit(request , pk , partial)
            else:
                return JsonResponse({"result" : "Bad Request"} , status = 400)
        else:
            return JsonResponse({"result" : "Bad Request"} , status = 400)
                
    def get_permissions(self):
        if self.action == "retrieve" or self.action == "approved":
            return [permissions.AllowAny(), ]
        return super(MushroomSpecimenViewSet, self).get_permissions()

    def retrieve(self, request, pk=None):
        if request.user.has_perm("view_mushroomspecimen"):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(approved = True)
        
        mushroom = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(mushroom)
        return JsonResponse(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])

        if request.user.has_perm("view_mushroomspecimen"):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(approved = True)

        result = helpers.search(queryset , params , MushroomSpecimenSerializer  , "OR")

        return JsonResponse(result, safe=False)

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])

        
        if request.user.has_perm("view_mushroomspecimen"):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(approved = True)

        result = helpers.search(queryset , params , MushroomSpecimenSerializer , "AND")

        return JsonResponse(result, safe=False)

    @action(methods=['get'] , detail=False)
    def approved(self, request , pk=None):
        result =  self.serializer_class(self.queryset.filter(approved=True), many = True).data
        return JsonResponse(result, safe=False)        


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

class NotificationDemoView(APIView):

    def get(self , request):
        helpers.send_notification("e9S99OJXnrrHr6AaESoZQ-:APA91bGm3ZiKbPEH2fzH7c2S4ctkcGozCIp_bZ5XnEsTqmoDG3BdQXdVFpAbE9g_HwuLwiwA7eljRTOgTEZvxJ89EV2b5iE8FpxYIg1avbL6mstPSKL_Dy2xkVMO2kUrZgI-PZBdvDtX")
        return JsonResponse({"result": "prueba"})
