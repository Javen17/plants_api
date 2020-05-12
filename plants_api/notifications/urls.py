from plants_api.notifications import views
from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'register_android_device' , views.AndroidNotificationDeviceViewSet)

urlpatterns = [
    path('', include(router.urls))     
]