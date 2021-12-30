from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class School(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


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
