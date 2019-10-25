from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from plants_api.main_site import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'main_site'

router = routers.DefaultRouter()


router.register(r'family', views.PlantFamilyViewSet)
router.register(r'species', views.PlantSpeciesViewSet)
router.register(r'specimen',views.PlantSpecimenViewSet)
router.register(r'recolector', views.RecolectorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^login/', obtain_auth_token)
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#     url(r'^$', views.IndexPageView.as_view(), name='index'),
]
