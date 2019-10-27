from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from plants_api.main_site import views
from plants_api.users import views as user_views

app_name = 'main_site'

router = routers.DefaultRouter()


router.register(r'family', views.PlantFamilyViewSet)
router.register(r'species', views.PlantSpeciesViewSet)
router.register(r'specimen',views.PlantSpecimenViewSet)
router.register(r'user', user_views.UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^login/', user_views.CustomObtainAuthToken.as_view()),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#     url(r'^$', views.IndexPageView.as_view(), name='index'),
]
