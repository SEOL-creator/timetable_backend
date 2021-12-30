from django.urls import path
from .views import *

urlpatterns = [
    path("", BoardView.as_view(), name="boardlist"),
    path("<str:board_code>/", ArticleListView.as_view(), name="articlelist"),
    path("reply/<int:reply_id>/like/", ReplyLikeView.as_view(), name="replylike"),
    path("reply/<int:reply_id>/", ReplyUpdateDeleteView.as_view(), name="reply"),
    path(
        "comments/<int:comment_id>/like/",
        CommentLikeView.as_view(),
        name="commentlike",
    ),
    path(
        "comments/<int:comment_id>/",
        CommentUpdateDeleteView.as_view(),
        name="commentupdatedelete",
    ),
    path(
        "article/<int:article_id>/comments/",
        CommentView.as_view(),
        name="articlecomments",
    ),
    path(
        "article/<int:article_id>/like/", ArticleLikeView.as_view(), name="articlelike"
    ),
    path("article/<int:article_id>/", ArticleView.as_view(), name="article"),
]
