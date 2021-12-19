from django.urls import path

from .views import *

urlpatterns = [
    path("", TimetableView.as_view(), name="timetable"),
    path("classroom/", ClassroomView.as_view(), name="classroomlist"),
    path("teacher/", TeacherListView.as_view(), name="teacherlist"),
    path("teacher/<int:id>", TeacherView.as_view(), name="teacher"),
    path(
        "classtime/<int:grade>/<int:room>/",
        ClassTimeView.as_view(),
        name="classtime",
    ),
    path(
        "tempclasstime/<int:grade>/<int:room>/",
        TempClassTimeView.as_view(),
        name="tempclasstime",
    ),
    path(
        "improvedtimetable/<int:grade>/<int:room>/<str:range>/",
        altered_timetable_view,
        name="testtimetable",
    ),
]
