from rest_framework import serializers
from .models import FrontVersion


class FrontVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontVersion
        fields = ("version", "note")
