from rest_framework import serializers
from .models import User , Profile
from django.contrib.auth.models import Permission , Group

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")
        #extra_kwargs = {'password': {'write_only': True, 'min_length': 4} , "user_permissions" : {'write_only': True} , "groups" : {'write_only': True}}

class GroupSerializer(serializers.ModelSerializer):
    #permissions = serializers.PrimaryKeyRelatedField(queryset= Permission.objects.all())

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'
