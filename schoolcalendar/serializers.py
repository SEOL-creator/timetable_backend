from rest_framework import serializers
from .models import *


class ScheduleSerializer(serializers.ModelSerializer):
    ordering_fields = ("start_date", "end_date")
    ordering = ("-start_date", "end_date")

    class Meta:
        model = Schedule
        fields = "__all__"
