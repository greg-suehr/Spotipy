from rest_framework import serializers
from tools.models import User, Library, Playlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uri', 'name', 'password', 'last_login']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['user']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['uri', 'user', 'name', 'created']
