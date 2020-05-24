from rest_framework.decorators import action
from plants_api.helpers import helpers
from urllib.parse import parse_qs
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import permissions

#Making them abstract would maybe be a good idea.

class BaseGoogleFixClass:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_action_classes = {
            'list':self.exclude_serializer,
            'retrieve':self.exclude_serializer
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs['partial'] = True

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class BaseSearchAndFilterClass:
    
    def get_permissions(self):
        if self.action in ["list" , "retrieve" , "search", "filter"]:
            return [permissions.AllowAny(), ]
        return super().get_permissions()
    
    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        return self.search_filter("OR")

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        return self.search_filter("AND")

    def search_filter(self, search_type):
        params = parse_qs(self.request.META['QUERY_STRING'])
        params.pop('page', None)

        if len(params) < 1:
            return JsonResponse({"result" : "Bad Request, at least one search parameter should be included"}, status = 400)
        
        try:
            result = helpers.search(self.get_queryset() , params , self.serializer_class  , search_type)
        except:
            return Response({"result" : "Invalid parameter for search"}, status = 400)

        page = self.paginate_queryset(result)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)



 
class BasePatchClass: 

    def edit(self, request ,  pk , partial):
        try:
            select_obj = self.model.objects.get(id=pk)
            serializer = self.serializer_class(select_obj, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return JsonResponse(serializer.data)
        except Exception as e:
            return JsonResponse({"result" : str(e)} , status = 400)

class SearchAndPatchMixin(BaseSearchAndFilterClass , BasePatchClass):
    pass
