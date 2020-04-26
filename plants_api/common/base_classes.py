from rest_framework.decorators import action
from plants_api.helpers import helpers
from urllib.parse import parse_qs
from django.http import JsonResponse

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
    
    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , self.serializer_class , "OR")
        return JsonResponse(result, safe=False)

    @action(methods=['get'], detail=False)
    def filter(self, request, pk=None):
        params = parse_qs(request.META['QUERY_STRING'])
        result = helpers.search(self.queryset , params , self.serializer_class  , "AND")
        return JsonResponse(result, safe=False)



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
