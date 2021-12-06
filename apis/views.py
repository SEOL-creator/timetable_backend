import datetime
from functools import partial
import json
import os
from django.contrib.auth.signals import user_logged_in
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import Q, query
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, generics, exceptions, serializers
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from accounts.serializers import (
    DetailedUserSerializer,
    RegisterSerializer,
    UserSerializer,
)
from accounts.models import User
from timetable.serializers import (
    ClassTimeSerializer,
    ClassroomSerializer,
    TeacherSerializer,
    TempClassSerializer,
    TimetableUseDateSerializer,
)
from timetable.models import (
    RemoteURL,
    TempClass,
    TimetableUseDate,
    Classroom,
    Teacher,
    ClassTime,
)

from schoolmeal.serializers import (
    MealSerializer,
    MealItemSerializer,
)
from schoolmeal.models import Meal, MealItem

from schoolcalendar.serializers import (
    ScheduleSerializer,
)
from schoolcalendar.models import Schedule
from usermemo.models import ToDoList, ToDoListComment
from usermemo.serializers import ToDoListSerializer, ToDoListCommentSerializer

UTC = datetime.timezone(datetime.timedelta(hours=0))


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
            serializer = UserSerializer(user)
            user_logged_in.send(sender=user.__class__, request=request, user=user)
        except Token.DoesNotExist:
            return JsonResponse({"valid": False}, status=200)
        return JsonResponse(
            {"valid": True, "user": serializer.data},
            status=200,
        )
    else:
        return JsonResponse(
            {"detail": f"""메소드(Method) "{request.method}"는 허용되지 않습니다."""}, status=405
        )


class UserListView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        queryset = User.objects.all().order_by("date_joined")
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, id):
        if id == "me":
            queryset = request.user
            serializer = DetailedUserSerializer(queryset)
        else:
            id = int(id)
            queryset = get_object_or_404(User, id=id)
            serializer = UserSerializer(queryset, read_only=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def user_profile_pic_upload(request):
    user = request.user
    image = request.FILES["image"]
    image_name = default_storage.save(
        os.path.join("profilepic", str(user.id), image.name.lower()), image
    )
    user.profilepic = image_name
    user.save(update_fields=["profilepic"])
    serializer = UserSerializer(user)
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
        with transaction.atomic():
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


@api_view(["GET"])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@renderer_classes((JSONRenderer,))
def asked_get_user_information(requset, userid):
    import requests

    url = f"https://asked.kr/query.php?query=4&id={userid}"
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        },
    )
    return Response(response.text, response.status_code)


@api_view(["GET"])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@renderer_classes((JSONRenderer,))
def asked_get_posts(requset, page, userid):
    import requests

    url = f"https://asked.kr/query.php?query=1&page={str(page)}&id={userid}"
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )
    response.encoding = "utf-8"
    return Response(response.text, response.status_code)


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
@renderer_classes((JSONRenderer,))
def asked_post_ask(requset):
    import requests

    url = f"https://asked.kr/query.php?query=0"
    response = requests.post(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        data=requset.body.decode("utf-8").encode("utf-8"),
    )

    return Response(response.text, response.status_code)


class TodoListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = ToDoList.objects.filter(deleted=False).order_by("-created_at")
        serializer = ToDoListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data.update({"author": request.user.id})
        serializer = ToDoListSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = get_object_or_404(ToDoList, pk=pk)
        todo.deleted = True
        todo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        todo = get_object_or_404(ToDoList, pk=pk)
        serializer = ToDoListSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoListCommentView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, todoid):
        queryset = ToDoListComment.objects.filter(todolist=todoid).order_by(
            "-created_at"
        )
        serializer = ToDoListCommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, todoid):
        request.data.update({"todolist": todoid})
        request.data.update({"author": request.user.id})
        serializer = ToDoListCommentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, commentid):
        comment = get_object_or_404(ToDoListComment, pk=commentid)
        comment.deleted = True
        comment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, todoid, commentid):
        comment = get_object_or_404(ToDoListComment, pk=commentid)
        serializer = ToDoListCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
