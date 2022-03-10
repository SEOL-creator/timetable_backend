import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "timetable_backend.settings.dev"
django.setup()

from timetable_v2.models import *


def insert_timetables():
    TimetableItem.objects.create(
        name="조회",
        start_time="08:50:00",
        end_time="09:00:00",
        timetable=Timetable.objects.get(id=1),
    )

    for j in range(1, 4):
        start_time_h = 9
        start_time_m = 00
        end_time_h = 9
        end_time_m = 10
        start_time_m += (j - 1) * 55
        if start_time_m >= 60:
            start_time_h += start_time_m // 60
            start_time_m -= start_time_m // 60 * 60
        end_time_m += (j - 1) * 55
        if end_time_m >= 60:
            end_time_h += end_time_m // 60
            end_time_m -= end_time_m // 60 * 60

        start_time_h = str(start_time_h).zfill(2)
        start_time_m = str(start_time_m).zfill(2)
        end_time_h = str(end_time_h).zfill(2)
        end_time_m = str(end_time_m).zfill(2)
        if j != 1:
            TimetableItem.objects.create(
                name=f"쉬는시간",
                start_time=f"{start_time_h}:{start_time_m}:00",
                end_time=f"{end_time_h}:{end_time_m}:00",
                timetable=Timetable.objects.get(id=1),
            )

        start_time_h = 9
        start_time_m = 10
        end_time_h = 9
        end_time_m = 55
        start_time_m += (j - 1) * 55
        if start_time_m >= 60:
            start_time_h += start_time_m // 60
            start_time_m -= start_time_m // 60 * 60
        end_time_m += (j - 1) * 55
        if end_time_m >= 60:
            end_time_h += end_time_m // 60
            end_time_m -= end_time_m // 60 * 60

        start_time_h = str(start_time_h).zfill(2)
        start_time_m = str(start_time_m).zfill(2)
        end_time_h = str(end_time_h).zfill(2)
        end_time_m = str(end_time_m).zfill(2)

        TimetableItem.objects.create(
            name=f"{j}교시",
            start_time=f"{start_time_h}:{start_time_m}:00",
            end_time=f"{end_time_h}:{end_time_m}:00",
            timetable=Timetable.objects.get(id=1),
        )

    TimetableItem.objects.create(
        name="점심",
        start_time="11:45:00",
        end_time="13:05:00",
        timetable=Timetable.objects.get(id=1),
    )

    for j in range(1, 5):
        start_time_h = 12
        start_time_m = 55
        end_time_h = 13
        end_time_m = 5
        start_time_m += (j - 1) * 55
        if start_time_m >= 60:
            start_time_h += start_time_m // 60
            start_time_m -= start_time_m // 60 * 60
        end_time_m += (j - 1) * 55
        if end_time_m >= 60:
            end_time_h += end_time_m // 60
            end_time_m -= end_time_m // 60 * 60

        start_time_h = str(start_time_h).zfill(2)
        start_time_m = str(start_time_m).zfill(2)
        end_time_h = str(end_time_h).zfill(2)
        end_time_m = str(end_time_m).zfill(2)
        if j != 1:
            TimetableItem.objects.create(
                name=f"쉬는시간",
                start_time=f"{start_time_h}:{start_time_m}:00",
                end_time=f"{end_time_h}:{end_time_m}:00",
                timetable=Timetable.objects.get(id=1),
            )

        start_time_h = 13
        start_time_m = 5
        end_time_h = 13
        end_time_m = 50
        start_time_m += (j - 1) * 55
        if start_time_m >= 60:
            start_time_h += start_time_m // 60
            start_time_m -= start_time_m // 60 * 60
        end_time_m += (j - 1) * 55
        if end_time_m >= 60:
            end_time_h += end_time_m // 60
            end_time_m -= end_time_m // 60 * 60

        start_time_h = str(start_time_h).zfill(2)
        start_time_m = str(start_time_m).zfill(2)
        end_time_h = str(end_time_h).zfill(2)
        end_time_m = str(end_time_m).zfill(2)

        TimetableItem.objects.create(
            name=f"{j + 3}교시",
            start_time=f"{start_time_h}:{start_time_m}:00",
            end_time=f"{end_time_h}:{end_time_m}:00",
            timetable=Timetable.objects.get(id=1),
        )
    TimetableItem.objects.create(
        name="청소 및 종례",
        start_time="16:35:00",
        end_time="16:50:00",
        timetable=Timetable.objects.get(id=1),
    )
    TimetableItem.objects.create(
        name="석식",
        start_time="16:50:00",
        end_time="17:50:00",
        timetable=Timetable.objects.get(id=1),
    )
    TimetableItem.objects.create(
        name="야자 1교시",
        start_time="17:50:00",
        end_time="19:50:00",
        timetable=Timetable.objects.get(id=1),
    )
    TimetableItem.objects.create(
        name="야자 2교시",
        start_time="20:00:00",
        end_time="21:30:00",
        timetable=Timetable.objects.get(id=1),
    )


def insert_colors():
    colors = (
        ("#e8554f", "Classic Red 1"),
        ("#c83a3a", "Classic Red 2"),
        ("#a91a27", "Classic Red 3"),
        ("#fcb345", "Classic Orange 1"),
        ("#fc992e", "Classic Orange 2"),
        ("#db7f28", "Classic Orange 3"),
        ("#fce862", "Classic Yellow 1"),
        ("#fccb4a", "Classic Yellow 2"),
        ("#dcb031", "Classic Yellow 3"),
        ("#8dde4f", "Classic Green 1"),
        ("#70c336", "Classic Green 2"),
        ("#55a628", "Classic Green 3"),
        ("#77c5de", "Classic Skyblue 1"),
        ("#5caac3", "Classic Skyblue 2"),
        ("#408fa7", "Classic Skyblue 3"),
        ("#688bf9", "Classic Blue 1"),
        ("#4972db", "Classic Blue 2"),
        ("#235bbe", "Classic Blue 3"),
        ("#c77bfa", "Classic Purple 1"),
        ("#aa61de", "Classic Purple 2"),
        ("#8e49c0", "Classic Purple 3"),
        ("#f77ebf", "Classic Pink 1"),
        ("#d964a4", "Classic Pink 2"),
        ("#bb4a8a", "Classic Pink 3"),
        ("#909090", "Classic Gray 1"),
        ("#777777", "Classic Gray 2"),
        ("#5f5f5f", "Classic Gray 3"),
    )

    for color in colors:
        Color.objects.create(
            color=color[0],
            name=color[1],
        )


insert_timetables()
insert_colors()
