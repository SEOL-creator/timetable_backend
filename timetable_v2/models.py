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


class Timetable(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="시정표 이름", null=False, blank=False
    )
    startdate = models.DateField(verbose_name="시정표 적용 시작 날짜", null=False, blank=False)

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


class StaticClass(models.Model):
    name = models.CharField(verbose_name="수업 이름", max_length=12, unique=True)
    short_name = models.CharField(verbose_name="축약 이름", max_length=3)
    teacher = models.ForeignKey(Teacher, verbose_name="담당 교사", on_delete=models.CASCADE)
    location = models.ForeignKey(
        Classroom,
        verbose_name="수업 교실",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    @property
    def place(self):
        if self.location:
            return self.location.name
        else:
            return ""


class FlexibleClass(models.Model):
    name = models.CharField(verbose_name="수업 이름", max_length=12, unique=True)
    short_name = models.CharField(verbose_name="축약 이름", max_length=3)
    teacher = models.ForeignKey(Teacher, verbose_name="담당 교사", on_delete=models.CASCADE)
    location = models.ForeignKey(
        Classroom,
        verbose_name="수업 교실",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

    @property
    def place(self):
        if self.location:
            return self.location.name
        return ""


class ClassTimetableMaster(models.Model):
    classroom = models.OneToOneField(
        Classroom,
        verbose_name="시간표를 만들 교실을 선택하세요.",
        on_delete=models.CASCADE,
    )


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
    class_static = models.ForeignKey(
        StaticClass, verbose_name="수업", on_delete=models.CASCADE, null=True, blank=True
    )
    class_flexible = models.ForeignKey(
        FlexibleClass,
        verbose_name="수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    @property
    def _class(self):
        if self.class_static:
            return self.class_static
        elif self.class_flexible:
            return self.class_flexible
        raise ValueError("No class")

    class Meta:
        unique_together = ("timetable", "day_of_week")


class ClassTimetableTempItem(models.Model):
    timetable = models.ForeignKey(
        ClassTimetableMaster,
        verbose_name="시간표",
        on_delete=models.CASCADE,
    )
    date = models.DateField(verbose_name="날짜")
    time = models.IntegerField(verbose_name="교시")
    class_static = models.ForeignKey(
        StaticClass, verbose_name="수업", on_delete=models.CASCADE, null=True, blank=True
    )
    class_flexible = models.ForeignKey(
        FlexibleClass,
        verbose_name="수업",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        return None

    class Meta:
        unique_together = ("timetable", "date", "time")
