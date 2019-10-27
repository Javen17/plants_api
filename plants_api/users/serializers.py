from rest_framework import serializers
from .models import User , Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):

    Profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'
