from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import CustomAuthToken


from . import views

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomAuthToken.as_view(), name="token"),
    path("timetable/", views.TimetableView.as_view(), name="timetable"),
    path("classroom/", views.ClassroomView.as_view(), name="classroomlist"),
    path("teacher/", views.TeacherListView.as_view(), name="teacherlist"),
    path("teacher/<int:id>", views.TeacherView.as_view(), name="teacher"),
    path(
        "classtime/<int:grade>/<int:room>/",
        views.ClassTimeView.as_view(),
        name="classtime",
    ),
    path(
        "tempclasstime/<int:grade>/<int:room>/",
        views.TempClassTimeView.as_view(),
        name="tempclasstime",
    ),
]
