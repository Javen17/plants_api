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
router.register(r'profile',user_views.ProfileViewSet)
router.register(r'group', user_views.GroupViewSet)
router.register(r'permission' , user_views.PermissionViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('permanent_login/', user_views.GeneratePermanentTokenView.as_view(), name = 'permanent_login')
    #path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #url(r'^login/', user_views.CustomObtainAuthToken.as_view()),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#     url(r'^$', views.IndexPageView.as_view(), name='index'),
]
