import datetime
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ClassTimeSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    TempClassSerializer,
    TimetableUseDateSerializer,
)
from .models import (
    RemoteURL,
    TempClass,
    TimetableUseDate,
    Classroom,
    Teacher,
    ClassTime,
)

UTC = datetime.timezone(datetime.timedelta(hours=0))


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
            ).order_by("startdate")
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
            (TODAY - datetime.timedelta(days=TODAY.weekday())).year,
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


@csrf_exempt
def altered_timetable_view(requset, grade, room, range):
    def ordinal_to_num(ordinal):
        if ordinal == "first":
            return 1
        elif ordinal == "second":
            return 2
        elif ordinal == "third":
            return 3
        elif ordinal == "fourth":
            return 4
        elif ordinal == "fifth":
            return 5
        elif ordinal == "sixth":
            return 6
        elif ordinal == "seventh":
            return 7
        return 0

    def get_class_time(table, classtime):
        data = {}
        data["start"] = table[0]["value"]
        data["end"] = table[1]["value"]

        if table[0]["field"].split("_")[0] in ("morning", "prepare", "lunch", "dinner"):
            data["type"] = "_".join(table[0]["field"].split("_")[:-1])
            return data

        else:
            time = ordinal_to_num(table[0]["field"].split("_")[0])
            remoteurl = RemoteURL.objects.filter(
                _class=classtime[time - 1]._class,
                classroom=classtime[time - 1].classroom,
            ).first()

            data["type"] = "class"
            data["time"] = time
            data["class"] = {
                "id": classtime[time - 1]._class.id,
                "teacher": {
                    "id": classtime[time - 1]._class.teacher.id,
                    "name": classtime[time - 1]._class.teacher.name,
                },
                "name": classtime[time - 1]._class.name,
                "short_name": classtime[time - 1]._class.short_name,
                "color": classtime[time - 1]._class.color,
            }
            if remoteurl and remoteurl.pcurl and remoteurl.mobileurl:
                data["class"]["remoteURL"] = {
                    "pc": remoteurl.pcurl,
                    "mobile": remoteurl.mobileurl,
                }

            return data

    classroom = get_object_or_404(Classroom, grade=grade, room=room)

    # Auth check
    try:
        user = TokenAuthentication().authenticate(requset)
    except exceptions.AuthenticationFailed as e:
        return JsonResponse({"detail": e.default_detail}, status=401)
    if user is None:
        return JsonResponse(
            {"detail": "You need to sign in to see this content."}, status=401
        )
    else:
        user = user[0]

    if range == "today":
        TODAY = datetime.datetime.today().date()
        if TODAY.weekday() > 4:
            TODAY = TODAY + datetime.timedelta(days=(7 - TODAY.weekday()))

        timetable = (
            TimetableUseDate.objects.filter(startdate__lte=TODAY)
            .order_by("-startdate")
            .first()
        )
        classtime = ClassTime.objects.filter(
            classroom=classroom, dayOfWeek=(TODAY.weekday() + 1)
        ).order_by("time")

        data = {}
        data["date"] = TODAY
        data["is_remote"] = timetable.is_remote
        data["classroom"] = {"grade": classroom.grade, "room": classroom.room}
        classTimetable = []

        temp = [{}, {}]
        for field in model_to_dict(timetable.timetable):
            if field == "id":
                continue
            if field == "name":
                continue

            if field.split("_")[-1:] == ["start"]:
                temp[0] = {
                    "field": field,
                    "value": timetable.timetable.__getattribute__(field),
                }
            if field.split("_")[-1:] == ["end"]:
                temp[1] = {
                    "field": field,
                    "value": timetable.timetable.__getattribute__(field),
                }
                classTimetable.append(get_class_time(temp, classtime))

        data["timetable"] = classTimetable

        return JsonResponse(data, status=200)

    elif range == "thisweek":
        TODAY = datetime.datetime.today().date()
        MONDAY = TODAY - datetime.timedelta(days=TODAY.weekday())
        FRIDAY = MONDAY + datetime.timedelta(days=4)
    elif range == "nextweek":
        pass
