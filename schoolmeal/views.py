import datetime
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import (
    MealSerializer,
    MealItemSerializer,
)
from .models import Meal, MealItem


class MealView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, year, month, day=0):
        if day == 0:
            queryset = Meal.objects.filter(date__year=year, date__month=month).order_by(
                "date", "type"
            )
            serializer = MealSerializer(queryset, many=True)
        else:
            queryset = Meal.objects.filter(
                date__year=year, date__month=month, date__day=day
            ).order_by("date", "type")
            serializer = MealSerializer(queryset, many=True)
        return Response(serializer.data)


class MealPostView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        year = request.data.get("date")[:4]
        month = request.data.get("date")[4:6]
        day = request.data.get("date")[6:]
        type = request.data.get("type")
        number_of_people = request.data.get("number_of_people")
        calories = request.data.get("calories")
        meal = Meal.objects.create(
            date=datetime.date(int(year), int(month), int(day)),
            type=int(type),
            number_of_people=int(number_of_people),
            calories=int(calories),
        )
        with transaction.atomic():
            for item in request.data.get("items"):
                MealItem.objects.create(
                    meal=meal,
                    name=item.get("name"),
                    allergy_codes=item.get("allergy_codes"),
                )

        return Response(status=201)
