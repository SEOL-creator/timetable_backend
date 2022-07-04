from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime

from .serializers import (
    ScheduleSerializer,
)
from .models import Schedule


class DdayView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = Schedule.objects.filter(
            is_registered_dday=True,
            end_date__gte=datetime.datetime.today(),
        ).order_by("start_date", "end_date")
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)
