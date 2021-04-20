from rest_framework import serializers
from tools.models import Library

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["username", "created", "updated"]
