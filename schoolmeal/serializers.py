from rest_framework import serializers
from .models import *


class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ("name", "allergy_codes")


class MealSerializer(serializers.ModelSerializer):
    meal_item = MealItemSerializer(many=True)

    ordering_fields = ("date", "type")
    ordering = ("date", "type")

    class Meta:
        model = Meal
        fields = ("date", "type", "number_of_people", "calories", "meal_item")
