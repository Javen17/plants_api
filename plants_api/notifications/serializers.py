from rest_framework import serializers
from push_notifications.models import GCMDevice

class AndroidNotificationDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = GCMDevice
        fields = '__all__'