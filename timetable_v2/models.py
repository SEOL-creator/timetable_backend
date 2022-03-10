from enum import unique
from django.db import models
from timetable.models import Classroom, Teacher
from django.utils.translation import ugettext as _


class DayOfTheWeek(models.IntegerChoices):
    MON = (
        1,
        _("Monday"),
    )
    TUE = (
        2,
        _("Tuesday"),
    )
    WED = (
        3,
        _("Wednesday"),
    )
    THU = (
        4,
        _("Thursday"),
    )
    FRI = (
        5,
        _("Friday"),
    )
    SAT = (
        6,
        _("Saturday"),
    )
    SUN = (
        7,
        _("Sunday"),
    )


class DayOfTheWeekField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = DayOfTheWeek.choices
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)


class Color(models.Model):
    color = models.CharField(
        verbose_name="색상 코드", max_length=7, null=False, blank=False
    )
    name = models.CharField(verbose_name="색상 이름", max_length=36)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="시정표 이름", null=False, blank=False
    )

    def __str__(self):
        return self.name


class TimetableItem(models.Model):
    name = models.CharField(
        max_length=20, verbose_name="시정표 항목 이름", null=False, blank=False
    )
    start_time = models.TimeField(verbose_name="시정표 항목 시작 시간", null=False, blank=False)
    end_time = models.TimeField(verbose_name="시정표 항목 종료 시간", null=False, blank=False)
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.timetable.name + " " + self.name


class TimetableWithDate(models.Model):
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, null=False, blank=False
    )
    startdate = models.DateField(verbose_name="시정표 적용 시작 날짜", null=False, blank=False)

    def __str__(self):
        return str(self.startdate) + " ~ " + self.timetable.name


class BaseClass(models.Model):
    name = models.CharField(verbose_name="수업 이름", max_length=12)
    short_name = models.CharField(verbose_name="수업 축약 이름", max_length=4)
    teacher = models.ForeignKey(Teacher, verbose_name="담당 교사", on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color,
        verbose_name="수업 색상",
        on_delete=models.SET_NULL,
        default=1,
        null=True,
        blank=False,
    )

    class Meta:
        abstract = True


class StaticClass(BaseClass):
    def __str__(self):
        return self.teacher.name + " " + self.name

    class Meta:
        unique_together = ("name", "teacher")


class FlexibleClass(BaseClass):
    name = models.CharField(verbose_name="수업 이름", max_length=12, unique=False)
    location_classroom = models.ForeignKey(
        Classroom,
        verbose_name="수업 교실",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    location_etc = models.CharField(
        verbose_name="수업 교실 (기타 경우)", max_length=30, null=True, blank=True
    )

    @property
    def location(self):
        if self.location_classroom:
            return self.location_classroom.name
        elif self.location_etc:
            return self.location_etc
        return ""

    def __str__(self):
        return self.location + " " + self.name + " " + self.teacher.name

    class Meta:
        unique_together = ("name", "location_classroom", "location_etc")


class TimeClass(BaseClass):
    time = models.CharField(
        max_length=1,
        verbose_name="타임",
        null=False,
        blank=False,
        default="A",
        choices=(("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")),
    )

    location_classroom = models.ForeignKey(
        Classroom,
        verbose_name="수업 교실",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    location_etc = models.CharField(
        verbose_name="수업 교실 (기타 경우)", max_length=30, null=True, blank=True
    )

    @property
    def location(self):
        if self.location_classroom:
            return self.location_classroom.name
        elif self.location_etc:
            return self.location_etc
        return ""

    def __str__(self):
        return self.time + "타임 " + self.name

    class Meta:
        unique_together = ("name", "time", "location_classroom", "location_etc")


class ClassTimetableMaster(models.Model):
    classroom = models.OneToOneField(
        Classroom,
        verbose_name="시간표를 만들 교실을 선택하세요.",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.classroom.name + " 시간표"


class ClassTimetableItem(models.Model):
    timetable = models.ForeignKey(
        ClassTimetableMaster,
        verbose_name="시간표",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    day_of_week = DayOfTheWeekField(verbose_name="요일")
    time = models.IntegerField(verbose_name="교시")
    type = models.CharField(
        max_length=8,
        verbose_name="수업 형식",
        null=False,
        blank=False,
        default="STATIC",
        choices=(("STATIC", "반 단위 수업"), ("FLEXIBLE", "이동 수업"), ("TIME", "타임형 수업")),
    )

    class_static = models.ForeignKey(
        StaticClass,
        verbose_name="반 단위 수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    class_flexible = models.ForeignKey(
        FlexibleClass,
        verbose_name="이동 수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    class_time = models.CharField(
        max_length=1,
        verbose_name="타임형 수업",
        null=True,
        blank=True,
        default="",
        choices=(("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")),
    )

    @property
    def _class(self):
        if self.class_static:
            return self.class_static
        elif self.class_flexible:
            return self.class_flexible
        elif self.class_time:
            return self.class_time
        raise ValueError("No class")

    def __str__(self):
        return (
            self.timetable.classroom.name
            + " "
            + self.get_day_of_week_display()
            + " "
            + str(self.time)
            + "교시 시간표 항목"
        )

    class Meta:
        unique_together = ("timetable", "day_of_week", "time")


class ClassTimetableTempItem(models.Model):
    timetable = models.ForeignKey(
        ClassTimetableMaster,
        verbose_name="시간표",
        on_delete=models.CASCADE,
    )
    date = models.DateField(verbose_name="날짜")
    time = models.IntegerField(verbose_name="교시")
    class_static = models.ForeignKey(
        StaticClass,
        verbose_name="반단위 수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    class_flexible = models.ForeignKey(
        FlexibleClass,
        verbose_name="이동 수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    class_time = models.CharField(
        max_length=1,
        verbose_name="타임형 수업",
        null=True,
        blank=True,
        default="",
        choices=(("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")),
    )

    class_temp_custom_name = models.CharField(
        verbose_name="사용자 지정 임시 수업 이름", max_length=12, null=True, blank=True
    )
    class_temp_custom_short_name = models.CharField(
        verbose_name="사용자 지정 임시 수업 축약 이름", max_length=3, null=True, blank=True
    )
    class_temp_custom_place = models.CharField(max_length=20, null=True, blank=True)

    @property
    def _class(self):
        if self.class_static:
            return self.class_static
        elif self.class_flexible:
            return self.class_flexible
        elif self.class_time:
            return self.class_time
        return None

    class Meta:
        unique_together = ("timetable", "date", "time")


class UserTimeClass(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        verbose_name="사용자",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    time = models.CharField(
        max_length=1,
        verbose_name="타임",
        null=False,
        blank=False,
        default="A",
        choices=(("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")),
    )
    _class = models.ForeignKey(
        TimeClass, verbose_name="수업", on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.user.nickname + " " + self.time + "타임 => " + self._class.name

    class Meta:
        unique_together = ("user", "time")


class UserClassTimetableItem(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        verbose_name="사용자",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    day_of_week = DayOfTheWeekField(verbose_name="요일")
    time = models.IntegerField(verbose_name="교시")

    _class = models.ForeignKey(
        FlexibleClass,
        verbose_name="이동 수업",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return (
            self.user.nickname
            + " "
            + self.get_day_of_week_display()
            + " "
            + str(self.time)
            + "교시 수업"
        )

    class Meta:
        unique_together = ("user", "day_of_week", "time")
