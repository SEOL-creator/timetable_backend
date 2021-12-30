from django.urls import path, include
from .views import frontVersionView, ReleaseNotesView

urlpatterns = [
    path("version/releases/", ReleaseNotesView.as_view(), name="releasenotes"),
    path("version/", frontVersionView, name="version"),
    path("accounts/", include("accounts.urls")),
    path("timetable/", include("timetable.urls")),
    path("meal/", include("schoolmeal.urls")),
    path("calendar/", include("schoolcalendar.urls")),
    path("asked/", include("asked.urls")),
    path("boards/", include("board.urls")),
]
