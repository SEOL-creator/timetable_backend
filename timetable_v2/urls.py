from django.urls import path

from .views import *

urlpatterns = [
    path("", TimetableView.as_view(), name="timetable"),
    path("classroom/", ClassroomView.as_view()),
    path("flexclasses/", FlexClassView.as_view(), name="possible_flex_classes"),
    path("timeclasses/", TimeClassView.as_view(), name="time_classes"),
    path("timeclasses/<str:time>/", TimeClassView.as_view(), name="time_classes_time"),
]
