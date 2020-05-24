from django.shortcuts import render
from push_notifications.models import GCMDevice
from plants_api.common.base_classes import ListSearchPatchMixin
from rest_framework import viewsets
from plants_api.notifications.serializers import AndroidNotificationDeviceSerializer
from rest_framework import permissions

# Create your views here.
class AndroidNotificationDeviceViewSet(ListSearchPatchMixin , viewsets.ModelViewSet):
    queryset = GCMDevice.objects.all()
    serializer_class = AndroidNotificationDeviceSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    

    def get_permissions(self):
        if self.action in ["update","create", "search" , "filter"] or self.request.method in ["PATCH", "PUT"]:
            return [permissions.AllowAny(), ]
        return super().get_permissions()
