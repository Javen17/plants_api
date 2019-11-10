from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from plants_api.main_site import views
from plants_api.users import views as user_views


app_name = 'main_site'

router = routers.DefaultRouter()

router.register(r'ecosystem' , views.EcosystemViewSet)
router.register(r'recolection_area_status' , views.RecolectionAreaStatusViewSet)
router.register(r'biostatus', views.BiostatusViewSet)
router.register(r'status' , views.StatusViewSet)
router.register(r'family', views.FamilyViewSet)
router.register(r'genus', views.GenusViewSet)
router.register(r'country',views.CountryViewSet)
router.register(r'state',views.StateViewSet)
router.register(r'city',views.CityViewSet)
router.register(r'mushroom_cap_type',views.CapTypeViewSet)
router.register(r'mushroom_form_type',views.FormTypeViewSet)
router.register(r'species', views.SpeciesViewSet)
router.register(r'plant_specimen',views.PlantSpecimenViewSet)
router.register(r'mushroom_specimen',views.MushroomSpecimenViewSet)
router.register(r'user', user_views.UserViewSet)
router.register(r'profile',user_views.ProfileViewSet)
router.register(r'group', user_views.GroupViewSet)
router.register(r'permission' , user_views.PermissionViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('permanent_login/', user_views.GeneratePermanentTokenView.as_view(), name = 'permanent_login'),
    path('delete_permanent_login/', user_views.RemovePermanentTokenView.as_view(), name = 'remove_permanent_token'),
    path('me/',user_views.WhoAmIView.as_view(), name = 'who_am_i')
    #path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #url(r'^login/', user_views.CustomObtainAuthToken.as_view()),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#     url(r'^$', views.IndexPageView.as_view(), name='index'),
]
