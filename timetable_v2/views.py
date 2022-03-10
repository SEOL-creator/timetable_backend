from .models import (
    ClassTimetableItem,
    ClassTimetableMaster,
    ClassTimetableTempItem,
    TimeClass,
    TimetableItem,
    TimetableWithDate,
    UserClassTimetableItem,
    UserTimeClass,
)
from timetable.models import Classroom
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import BadRequest
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import re


class TimetableView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def __get_timetabble(self, MON_DATE):
        timetables = []
        for i in range(0, 5):
            timetable = (
                TimetableWithDate.objects.order_by("-startdate")
                .filter(Q(startdate__lte=MON_DATE + datetime.timedelta(days=i)))
                .first()
            )
            if not timetable:
                timetables.append([])
            else:
                timetable_items = (
                    TimetableItem.objects.filter(
                        timetable=timetable.timetable,
                    )
                    .order_by("start_time")
                    .all()
                )
                timetables.append(timetable_items)
        return timetables

    def get(self, request, week="this"):
        user = request.user
        classroom = user.classroom
        if classroom is None:
            raise BadRequest("User is not in a classroom")

        CURRENT_DATE = timezone.now()
        FIRST_DATE_OF_WEEK = timezone.now().date() - datetime.timedelta(
            days=timezone.now().weekday()
        )
        TIMETABLES = self.__get_timetabble(FIRST_DATE_OF_WEEK)
        CLASS_TIMETABLE = ClassTimetableMaster.objects.filter(
            classroom=classroom
        ).first()

        result = {
            "classroom": user.classroom.name,
            "days": [[], [], [], [], []],
        }

        for day, timetable_of_day in enumerate(TIMETABLES):
            for timetable in timetable_of_day:
                _class = None
                timetable_item_object = None
                if re.match("^[0-9]교시$", timetable.name):
                    time = int(timetable.name[:1])  # 교시
                    temp_class = ClassTimetableTempItem.objects.filter(
                        timetable=CLASS_TIMETABLE,
                        date=FIRST_DATE_OF_WEEK + datetime.timedelta(days=day),
                        time=time,
                    ).all()
                    if len(temp_class) > 0:
                        pass
                    else:
                        class_timetable_item = ClassTimetableItem.objects.filter(
                            timetable=CLASS_TIMETABLE, day_of_week=day + 1, time=time
                        ).first()
                        if class_timetable_item is not None:
                            if class_timetable_item.type == "STATIC":
                                _class = {
                                    "type": "static",
                                    "name": class_timetable_item._class.name,
                                    "short_name": class_timetable_item._class.short_name,
                                    "teacher": {
                                        "id": class_timetable_item._class.teacher.id,
                                        "name": class_timetable_item._class.teacher.name,
                                    },
                                    "location": classroom.name,
                                    "color": class_timetable_item._class.color.color,
                                }
                            elif class_timetable_item.type == "FLEXIBLE":
                                user_selected_class = (
                                    UserClassTimetableItem.objects.filter(
                                        user=user,
                                        day_of_week=day + 1,
                                        time=time,
                                    ).first()
                                )
                                if user_selected_class is None:
                                    _class = {
                                        "type": "flexible_not_chosen",
                                        "name": "",
                                        "short_name": "",
                                        "teacher": {
                                            "id": "",
                                            "name": "",
                                        },
                                        "location": "",
                                        "color": "",
                                    }
                                else:
                                    _class = {
                                        "type": "flexible",
                                        "name": user_selected_class._class.name,
                                        "short_name": user_selected_class._class.short_name,
                                        "teacher": {
                                            "id": user_selected_class._class.teacher.id,
                                            "name": user_selected_class._class.teacher.name,
                                        },
                                        "location": user_selected_class._class.location,
                                        "color": user_selected_class._class.color.color,
                                    }
                            elif class_timetable_item.type == "TIME":
                                user_selected_class = UserTimeClass.objects.filter(
                                    user=user,
                                    time=class_timetable_item._class,
                                ).first()
                                if user_selected_class is None:
                                    _class = {
                                        "type": "time_not_chosen",
                                        "name": "",
                                        "short_name": "",
                                        "teacher": {
                                            "id": "",
                                            "name": "",
                                        },
                                        "location": "",
                                        "color": "",
                                    }
                                else:
                                    _class = {
                                        "type": "time",
                                        "time": user_selected_class.time,
                                        "name": user_selected_class._class.name,
                                        "short_name": user_selected_class._class.short_name,
                                        "teacher": {
                                            "id": user_selected_class._class.teacher.id,
                                            "name": user_selected_class._class.teacher.name,
                                        },
                                        "location": user_selected_class._class.location,
                                        "color": user_selected_class._class.color.color,
                                    }

                    timetable_item_object = {
                        "name": timetable.name,
                        "start_time": f"{str(timetable.start_time.hour).zfill(2)}:{str(timetable.start_time.minute).zfill(2)}:00",
                        "end_time": f"{str(timetable.end_time.hour).zfill(2)}:{str(timetable.end_time.minute).zfill(2)}:00",
                        "time": int(timetable.name[:1]),
                        "class": _class,
                    }

                else:
                    timetable_item_object = {
                        "name": timetable.name,
                        "start_time": f"{str(timetable.start_time.hour).zfill(2)}:{str(timetable.start_time.minute).zfill(2)}:00",
                        "end_time": f"{str(timetable.end_time.hour).zfill(2)}:{str(timetable.end_time.minute).zfill(2)}:00",
                        "class": None,
                    }
                result["days"][day].append(timetable_item_object)
        return Response(result)


class FlexClassView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        classroom = user.classroom
        day = int(request.query_params.get("day"))
        time = int(request.query_params.get("time"))

        classes = (
            ClassTimetableItem.objects.filter(
                timetable__classroom__grade=classroom.grade,
                day_of_week=day + 1,
                time=time,
            )
            .order_by("timetable__classroom__grade", "timetable__classroom__room")
            .all()
        )

        result = []
        for _class in classes:
            if _class.type != "FLEXIBLE":
                continue
            result.append(
                {
                    "timetableitem_id": _class.id,
                    "name": _class._class.name,
                    "short_name": _class._class.short_name,
                    "teacher": {
                        "id": _class._class.teacher.id,
                        "name": _class._class.teacher.name,
                    },
                    "location": ""
                    if not _class._class.location
                    else _class._class.location,
                    "color": _class._class.color.color,
                }
            )

        return Response(result)

    def post(self, request):
        id = request.data.get("timetable_id")

        classtimetableitem = ClassTimetableItem.objects.get(id=id)

        UserClassTimetableItem.objects.create(
            user=request.user,
            timetable=classtimetableitem.timetable,
            day_of_week=classtimetableitem.day_of_week,
            time=classtimetableitem.time,
            _class=classtimetableitem._class,
        )

        return Response(status=status.HTTP_200_OK)


class ClassroomView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        classroom_id = int(request.data.get("classroom_id"))

        user.classroom = Classroom.objects.get(id=classroom_id)
        user.save()
        UserClassTimetableItem.objects.filter(user=user).delete()

        return Response(status=status.HTTP_200_OK)


class TimeClassView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        result = {
            "list": {"A": [], "B": [], "C": [], "D": []},
            "user_selected": {
                "A": None,
                "B": None,
                "C": None,
                "D": None,
            },
        }
        for _class in TimeClass.objects.all():
            result["list"][_class.time].append(
                {
                    "id": _class.id,
                    "name": _class.name,
                    "short_name": _class.short_name,
                    "teacher": {
                        "id": _class.teacher.id,
                        "name": _class.teacher.name,
                    },
                    "location": _class.location,
                    "color": _class.color.color,
                }
            )
        for _class in UserTimeClass.objects.filter(user=user).all():
            result["user_selected"][_class.time] = _class.id
        return Response(result)

    def post(self, request, time):
        user = request.user
        class_id = int(request.data.get("class_id"))

        user_time_class = UserTimeClass.objects.filter(
            user=user,
            time=time,
        ).first()
        if user_time_class is not None:
            user_time_class.delete()

        UserTimeClass.objects.create(
            user=user,
            time=time,
            _class=TimeClass.objects.get(id=class_id),
        )

        return Response(status=status.HTTP_200_OK)
