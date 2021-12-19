from django.urls import path
from .views import *

urlpatterns = [
    path("<int:year>/<int:month>/<int:day>/", MealView.as_view(), name="meal"),
    path("<int:year>/<int:month>/", MealView.as_view(), name="meal"),
    path("", MealPostView.as_view(), name="postmeal"),
]
