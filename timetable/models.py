from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
    name = models.CharField(verbose_name="시정표 이름", max_length=12)
    morning_meeting_start = models.TimeField(verbose_name="조회 시작 시간")
    morning_meeting_end = models.TimeField(verbose_name="조회 종료 시간")
    prepare_start = models.TimeField(verbose_name="수업 준비 시작 시간")
    prepare_end = models.TimeField(verbose_name="수업 준비 종료 시간")
    first_start = models.TimeField(verbose_name="1교시 시작 시간")
    first_end = models.TimeField(verbose_name="1교시 종료 시간")
    second_start = models.TimeField(verbose_name="2교시 시작 시간")
    second_end = models.TimeField(verbose_name="2교시 종료 시간")
    third_start = models.TimeField(verbose_name="3교시 시작 시간")
    third_end = models.TimeField(verbose_name="3교시 종료 시간")
    lunch_start = models.TimeField(verbose_name="중식 시작 시간")
    lunch_end = models.TimeField(verbose_name="중식 종료 시간")
    fourth_start = models.TimeField(verbose_name="4교시 시작 시간")
    fourth_end = models.TimeField(verbose_name="4교시 종료 시간")
    fifth_start = models.TimeField(verbose_name="5교시 시작 시간")
    fifth_end = models.TimeField(verbose_name="5교시 종료 시간")
    sixth_start = models.TimeField(verbose_name="6교시 시작 시간")
    sixth_end = models.TimeField(verbose_name="6교시 종료 시간")
    seventh_start = models.TimeField(verbose_name="7교시 시작 시간")
    seventh_end = models.TimeField(verbose_name="7교시 종료 시간")
    dinner_start = models.TimeField(verbose_name="석식 시작 시간")
    dinner_end = models.TimeField(verbose_name="석식 종료 시간")

    def __str__(self):
        return self.name


class TimetableUseDate(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    is_remote = models.BooleanField(default=False)
    startdate = models.DateField(verbose_name="적용 시작 날짜")

    def __str__(self):
        return f"{self.timetable.name} {self.startdate}"


class Classroom(models.Model):
    class Grade(models.IntegerChoices):
        FIRST = 1, "1학년"
        SECOND = 2, "2학년"
        THIRD = 3, "3학년"

    grade = models.IntegerField(
        verbose_name="학년", choices=Grade.choices, default=Grade.FIRST
    )
    room = models.IntegerField(
        verbose_name="반",
        default=1,
        validators=[MaxValueValidator(12), MinValueValidator(1)],
    )

    def __str__(self):
        return f"{self.get_grade_display()} {self.room}반"


class Office(models.Model):
    name = models.CharField(verbose_name="교무실", max_length=16, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(verbose_name="소속/역할", max_length=16, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(verbose_name="이름", max_length=10)
    homeroom = models.ForeignKey(
        Classroom, blank=True, null=True, on_delete=models.SET_NULL
    )
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return f"{self.name} {self.office}"


class Class(models.Model):
    name = models.CharField(verbose_name="수업 이름", max_length=12, unique=True)
    short_name = models.CharField(verbose_name="축약 이름", max_length=3)
    teacher = models.ForeignKey(Teacher, verbose_name="담당 교사", on_delete=models.CASCADE)
    color = models.CharField(verbose_name="색상 코드", max_length=7)

    def __str__(self):
        return f"{self.name}, {self.teacher.name}"


class ClassTime(models.Model):
    _class = models.ForeignKey(Class, verbose_name="수업", on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, verbose_name="대상 학급", on_delete=models.CASCADE
    )

    class Time(models.IntegerChoices):
        FIRST = 1, "1교시"
        SECOND = 2, "2교시"
        THIRD = 3, "3교시"
        FOURTH = 4, "4교시"
        FIFTH = 5, "5교시"
        SIXTH = 6, "6교시"
        SEVENTH = 7, "7교시"

    time = models.IntegerField(
        verbose_name="교시", choices=Time.choices, default=Time.FIRST
    )

    dayOfWeek = DayOfTheWeekField(verbose_name="요일", default=DayOfTheWeek.MON)

    def __str__(self):
        return (
            f"{self.classroom} {self.get_dayOfWeek_display()} {self.get_time_display()}"
        )


class TempClass(models.Model):
    _class = models.ForeignKey(
        Class, verbose_name="수업", on_delete=models.CASCADE, blank=True, null=True
    )
    date = models.DateField(verbose_name="변경 대상 날짜")
    classroom = models.ForeignKey(
        Classroom, verbose_name="대상 학급", on_delete=models.CASCADE
    )

    class Time(models.IntegerChoices):
        FIRST = 1, "1교시"
        SECOND = 2, "2교시"
        THIRD = 3, "3교시"
        FOURTH = 4, "4교시"
        FIFTH = 5, "5교시"
        SIXTH = 6, "6교시"
        SEVENTH = 7, "7교시"

    time = models.IntegerField(
        verbose_name="교시", choices=Time.choices, default=Time.FIRST
    )

    def __str__(self):
        return f"{self.date} {self.classroom} {self.get_time_display()}"


class RemoteURL(models.Model):
    _class = models.ForeignKey(Class, verbose_name="수업", on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, verbose_name="학급", on_delete=models.CASCADE
    )
    url = models.CharField(max_length=600, verbose_name="URL")

    def __str__(self):
        return f"{self.classroom} {self._class.name}"
