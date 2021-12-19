from django.urls import path
from .views import *

urlpatterns = [
    path("token/", CustomAuthToken.as_view(), name="token"),
    path("register/", RegisterView.as_view(), name="register"),
    path("validatetoken/", validateToken, name="validatetoken"),
    path("users/", UserListView.as_view(), name="userlist"),
    path(
        "users/uploadprofilepic/",
        user_profile_pic_upload,
        name="uploadprofilepic",
    ),
    path("users/<str:id>/", UserView.as_view(), name="user"),
]
