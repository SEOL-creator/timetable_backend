from django.urls import path

from .views import *

urlpatterns = [
    path(
        "userinfo/<str:userid>/",
        asked_get_user_information,
        name="asked_userinfo",
    ),
    path(
        "posts/<str:userid>/<int:page>/",
        asked_get_posts,
        name="asked_posts",
    ),
    path(
        "ask/",
        asked_post_ask,
        name="asked_ask",
    ),
]
