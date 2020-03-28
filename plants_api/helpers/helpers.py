from django.db.models import Q
from django.utils.crypto import get_random_string

def search(queryset , search_dic , serializer , type):
#    first_search , *searchs = search_dic
    filter_field , *filters = search_dic.keys()
    search_field , *fields = search_dic.values()

    if search_field is not None and filter_field is not None:
        q_objects = Q()
        q_objects = Q(**{ filter_field + '__icontains' : search_field[0] })

        if len(search_dic) > 1 :

            if type == "OR":
                for filter , field in zip(filters, fields):
                    q_objects |= Q(**{ filter + '__icontains' : field[0]})
            elif type == "AND":
                for filter , field in zip(filters, fields):
                    q_objects &= Q(**{ filter + '__icontains' : field[0]})

        found_elements = queryset.filter(q_objects)
        resultlist = []

        for found in found_elements:
            serializers = serializer(found)
            resultlist.append(serializers.data)

        return resultlist
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


def get_temporal_password(user):
    unique_id = get_random_string(length=32)
    user.temporal_password = unique_id
    user.save()
    return unique_id