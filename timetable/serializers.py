from rest_framework import serializers
from .models import *


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = "__all__"


class TimetableUseDateSerializer(serializers.ModelSerializer):
    timetable = TimetableSerializer(read_only=True)

    class Meta:
        model = TimetableUseDate
        fields = ("is_remote", "startdate", "timetable")


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "grade", "room")


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    homeroom = ClassroomSerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ("name", "homeroom", "office", "role")


class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "name")


class ClassSerializer(serializers.ModelSerializer):
    teacher = SimpleTeacherSerializer(read_only=True)

    class Meta:
        model = Class
        fields = "__all__"


class ClassTimeSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(read_only=True)
    # classroom = ClassroomSerializer(read_only=True)

    remoteURL = serializers.SerializerMethodField()
    classtingURL = serializers.SerializerMethodField()

    def get_remoteURL(self, obj):
        urlOBJ = RemoteURL.objects.filter(_class=obj._class, classroom=obj.classroom)
        if urlOBJ:
            return {"pc": urlOBJ[0].pcurl, "mobile": urlOBJ[0].mobileurl}
        else:
            return ""

    def get_classtingURL(self, obj):
        urlOBJ = ClasstingURL.objects.filter(_class=obj._class, classroom=obj.classroom)
        if urlOBJ:
            return urlOBJ[0].classtingurl
        else:
            return ""

    class Meta:
        model = ClassTime
        fields = ("dayOfWeek", "time", "_class", "remoteURL", "classtingURL")


class TempClassSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    remoteURL = serializers.SerializerMethodField()

    def get_remoteURL(self, obj):
        urlOBJ = RemoteURL.objects.filter(_class=obj._class, classroom=obj.classroom)
        if urlOBJ:
            return {"pc": urlOBJ[0].pcurl, "mobile": urlOBJ[0].mobileurl}
        else:
            return ""

    class Meta:
        model = TempClass
        fields = "__all__"
