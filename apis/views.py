import datetime
import json
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.serializers import RegisterSerializer, UserSerializer
from accounts.models import User
from timetable.serializers import (
    ClassTimeSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    TempClassSerializer,
    TimetableUseDateSerializer,
)
from timetable.models import TempClass, TimetableUseDate, Classroom, Teacher, ClassTime

from schoolmeal.serializers import (
    MealSerializer,
    MealItemSerializer,
)
from schoolmeal.models import Meal, MealItem

from schoolcalendar.serializers import (
    ScheduleSerializer,
)
from schoolcalendar.models import Schedule

UTC = datetime.timezone(datetime.timedelta(hours=0))


@api_view(["GET"])
def User_View(request):
    if request.method == "GET":
        queryset = request.user
        serializer = UserSerializer(queryset)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


@csrf_exempt
def validateToken(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            token = Token.objects.get(key=data["token"])
            user = token.user
            user_logged_in.send(sender=user.__class__, request=request, user=user)
        except Token.DoesNotExist:
            return JsonResponse({"valid": False}, status=200)
        return JsonResponse(
            {"valid": True, "user": {"email": user.email, "nickname": user.nickname}},
            status=200,
        )


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
    def get(self, request, grade, room):
        classroom = get_object_or_404(Classroom, grade=grade, room=room)
        queryset = ClassTime.objects.filter(classroom=classroom).order_by(
            "dayOfWeek", "time"
        )
        serializer = ClassTimeSerializer(queryset, many=True)
        return Response(serializer.data)


class TempClassTimeView(APIView):
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


class MealView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, year, month, day=0):
        if day == 0:
            queryset = Meal.objects.filter(date__year=year, date__month=month).order_by(
                "date", "type"
            )
            print(queryset)
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
        for item in request.data.get("items"):
            MealItem.objects.create(
                meal=meal,
                name=item.get("name"),
                allergy_codes=item.get("allergy_codes"),
            )

        return Response(status=201)


class DdayView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = Schedule.objects.filter(is_registered_dday=True).order_by(
            "start_date", "end_date"
        )
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)
