from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import CustomAuthToken


from . import views

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomAuthToken.as_view(), name="token"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("validatetoken/", views.validateToken, name="validatetoken"),
    path("users/", views.UserListView.as_view(), name="userlist"),
    path(
        "users/uploadprofilepic/",
        views.user_profile_pic_upload,
        name="uploadprofilepic",
    ),
    path("users/<str:id>/", views.UserView.as_view(), name="user"),
    path("classroom/", views.ClassroomView.as_view(), name="classroomlist"),
    path("teacher/", views.TeacherListView.as_view(), name="teacherlist"),
    path("teacher/<int:id>", views.TeacherView.as_view(), name="teacher"),
    path("timetable/", views.TimetableView.as_view(), name="timetable"),
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
    path(
        "meal/<int:year>/<int:month>/<int:day>/", views.MealView.as_view(), name="meal"
    ),
    path("meal/<int:year>/<int:month>/", views.MealView.as_view(), name="meal"),
    path("meal/", views.MealPostView.as_view(), name="postmeal"),
    path("dday/", views.DdayView.as_view(), name="dday"),
    path(
        "improvedtimetable/<int:grade>/<int:room>/<str:range>/",
        views.altered_timetable_view,
        name="testtimetable",
    ),
    path(
        "asked/userinfo/<str:userid>/",
        views.asked_get_user_information,
        name="asked_userinfo",
    ),
    path(
        "asked/posts/<str:userid>/<int:page>/",
        views.asked_get_posts,
        name="asked_posts",
    ),
    path(
        "asked/ask/",
        views.asked_post_ask,
        name="asked_ask",
    ),
    path("todolist/", views.TodoListView.as_view(), name="todolist"),
    path("todolist/<int:pk>/", views.TodoListView.as_view(), name="todolistwithid"),
    path(
        "todolist/<int:todoid>/comments/",
        views.ToDoListCommentView.as_view(),
        name="todolistcomment",
    ),
    path(
        "todolist/<int:todoid>/comments/<int:commentid>/",
        views.ToDoListCommentView.as_view(),
        name="todolistcommentwithid",
    ),
]
