from django.db.models import Q

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
