import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from accounts.models import User
from timetable.serializers import (
    ClassTimeSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    TempClassSerializer,
    TimetableUseDateSerializer,
)
from timetable.models import TempClass, TimetableUseDate, Classroom, Teacher, ClassTime

UTC = datetime.timezone(datetime.timedelta(hours=0))

def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
def User_View(request):
    if request.method == "GET":
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data)


class TimetableView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        querydate = request.GET.get("date")
        TODAY = timezone.now()
        if querydate == "current":
            try:
                queryset = TimetableUseDate.objects.filter(
                    startdate__lte=TODAY
                ).order_by("-startdate")[:1]
            except IndexError:
                queryset = TimetableUseDate.objects.none()
        else:
            queryset = TimetableUseDate.objects.filter(
                Q(startdate__lte=TODAY) | Q(startdate__gt=TODAY)
            )
        serializer = TimetableUseDateSerializer(queryset, many=True)
        return Response(serializer.data)


class ClassroomView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = Classroom.objects.all().order_by("grade", "room")
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data)


class TeacherListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = Teacher.objects.all()
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)


class TeacherView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, id):
        queryset = get_object_or_404(Teacher, id=id)
        serializer = TeacherSerializer(queryset)
        return Response(serializer.data)


class ClassTimeView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, grade, room):
        classroom = get_object_or_404(Classroom, grade=grade, room=room)
        queryset = ClassTime.objects.filter(classroom=classroom).order_by(
            "dayOfWeek", "time"
        )
        serializer = ClassTimeSerializer(queryset, many=True)
        return Response(serializer.data)


class TempClassTimeView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, grade, room):
        classroom = get_object_or_404(Classroom, grade=grade, room=room)
        TODAY = timezone.now()
        MONDAY = datetime.datetime(
            TODAY.year,
            (TODAY - datetime.timedelta(days=TODAY.weekday())).month,
            (TODAY - datetime.timedelta(days=TODAY.weekday())).day,
            0,
            0,
            0,
            0,
            tzinfo=UTC,
        )
        NEXTFRIDAY = MONDAY + datetime.timedelta(days=11)
        queryset = TempClass.objects.filter(
            classroom=classroom, date__lte=NEXTFRIDAY, date__gte=MONDAY
        ).order_by("date")
        serializer = TempClassSerializer(queryset, many=True)
        return Response(serializer.data)
