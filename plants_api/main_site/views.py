from django.shortcuts import render
from .models import Ecosystem , RecolectionAreaStatus , Biostatus , Status ,  Species, Family , Genus , Country , State ,  City , CapType , FormType , PlantSpecimen , MushroomSpecimen
from plants_api.users.models import User
from plants_api.users.views import UserViewSet
from plants_api.users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import EcosystemSerializer, RecolectionAreaStatusSerializer , BiostatusSerializer , StatusSerializer , SpeciesSerializer, FamilySerializer , GenusSerializer , CountrySerializer, StateSerializer , CitySerializer , CapTypeSerializer , FormTypeSerializer , PlantSpecimenSerializer , MushroomSpecimenSerializer
from django.http import HttpResponse , JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from rest_framework import permissions
from plants_api.helpers import helpers
from urllib.parse import parse_qs

#from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView

class EcosystemViewSet(viewsets.ModelViewSet):
    queryset = Ecosystem.objects.all()
    serializer_class = EcosystemSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , EcosystemSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , EcosystemSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(EcosystemViewSet, self).get_permissions()


class RecolectionAreaStatusViewSet(viewsets.ModelViewSet):
    queryset = RecolectionAreaStatus.objects.all()
    serializer_class = RecolectionAreaStatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , RecolectionAreaStatusSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , RecolectionAreaStatusSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(RecolectionAreaStatusViewSet, self).get_permissions()

class BiostatusViewSet(viewsets.ModelViewSet):
    queryset = Biostatus.objects.all()
    serializer_class = BiostatusSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , BiostatusSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , BiostatusSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(BiostatusViewSet, self).get_permissions()


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , StatusSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , StatusSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(StatusViewSet, self).get_permissions()


class FamilyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , FamilySerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , FamilySerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(FamilyViewSet, self).get_permissions()

class GenusViewSet(viewsets.ModelViewSet):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , GenusSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , GenusSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(GenusViewSet, self).get_permissions()


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CountrySerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CountrySerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CountryViewSet, self).get_permissions()


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , StateSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , StateSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(StateViewSet, self).get_permissions()


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CitySerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CitySerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CityViewSet, self).get_permissions()

class CapTypeViewSet(viewsets.ModelViewSet):
    queryset = CapType.objects.all()
    serializer_class = CapTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CapTypeSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , CapTypeSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(CapTypeViewSet, self).get_permissions()


class FormTypeViewSet(viewsets.ModelViewSet):
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]


    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , FormTypeSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , FormTypeSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(FormTypeViewSet, self).get_permissions()

class SpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = SpeciesSerializer
    queryset = Species.objects.all()
    parser_class = (FileUploadParser,)

    permission_classes = [permissions.DjangoModelPermissions]

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , SpeciesSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , SpeciesSerializer , "AND")

        return JsonResponse({"result": result})

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(SpeciesViewSet, self).get_permissions()

#class SpecimenStatusViewSet(viewsets.ModelViewSet):
#    serializer_class = SpecimenStatusSerializer
#    queryset = SpecimenStatus



class PlantSpecimenViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSpecimenSerializer
    queryset = PlantSpecimen.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]

    def update(self, request , pk = None):

        if pk is not None:

            approved = request.data.get("approved")

            if request.user.has_perm("change_plant_approval") and approved:
                return super(PlantSpecimenViewSet, self).update(request , pk)
            elif approved is None:
                return super(PlantSpecimenViewSet, self).update(request , pk)
            else:
                return JsonResponse({"result": "Unauthorized"} , status = 401)
            #except:
                #return super(PlantSpecimenViewSet, self).update(request , pk)


    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(PlantSpecimenViewSet, self).get_permissions()

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , PlantSpecimenSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , PlantSpecimenSerializer , "AND")

        return JsonResponse({"result": result})



class MushroomSpecimenViewSet(viewsets.ModelViewSet):
    queryset = MushroomSpecimen.objects.all()
    serializer_class = MushroomSpecimenSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def update(self , request, pk = None):

        if pk is not None:

            approved = request.data.get("approved")

            if request.user.has_perm("change_mushroom_approval") and approved:
                return super(MushroomSpecimenViewSet, self).update(request , pk)
            elif approved is None:
                return super(MushroomSpecimenViewSet, self).update(request , pk)
            else:
                return JsonResponse({"result": "Unauthorized"} , status = 401)

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.AllowAny(), ]
        return super(MushroomSpecimenViewSet, self).get_permissions()

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , GroupSerializer , "OR")

        return JsonResponse({"result": result})

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , GroupSerializer , "AND")

        return JsonResponse({"result": result})
