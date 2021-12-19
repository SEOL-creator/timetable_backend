from django.urls import path
from .views import *

urlpatterns = [
    path("dday/", DdayView.as_view(), name="dday"),
]
