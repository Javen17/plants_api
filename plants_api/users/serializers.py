from rest_framework import serializers
from .models import User , Profile
from django.contrib.auth.models import Permission , Group

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileExcludeSerializer(ProfileSerializer):

    class Meta:
        model = Profile
        exclude = ('photo' , )

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    def to_internal_value(self, data):
        self.fields['profile'] = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
        return super(UserSerializer, self).to_internal_value(data)

    def to_representation(self, obj):
        self.fields['profile'] = ProfileSerializer()
        return super(UserSerializer, self).to_representation(obj)

    class Meta:
        model = User
        exclude = ("password", "user_permissions" , "temporal_password")
        #extra_kwargs = {'password': {'write_only': True, 'min_length': 4} , "user_permissions" : {'write_only': True} , "groups" : {'write_only': True}}


class UserExcludeSerializer(UserSerializer):

    def to_representation(self, obj):
        self.fields['profile'] = ProfileExcludeSerializer()
        return super(UserSerializer, self).to_representation(obj)

    class Meta:
        model = User
        exclude = ("password", "user_permissions" , "temporal_password")

class GroupSerializer(serializers.ModelSerializer):
    #permissions = serializers.PrimaryKeyRelatedField(queryset= Permission.objects.all())

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'
