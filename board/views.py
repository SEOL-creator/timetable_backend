from django.core.files.storage import default_storage
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, permissions, status
from .models import *
from .serializers import *


class BoardView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request):
        queryset = Board.objects.all().order_by("created_at")
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request, board_code):
        queryset = Article.objects.filter(
            board__code=board_code, is_deleted=False
        ).order_by("-id")
        serializer = ArticleSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, board_code):
        board = get_object_or_404(Board, code=board_code)
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data.update({"author": request.user.id})
        request.data.update({"board": board_code})
        if board.type == "ANON":
            request.data.update({"is_anonymous": True})
        elif board.type == "REAL":
            request.data.update({"is_anonymous": False})

        vote = None
        if "vote" in request.data:
            vote = request.data.pop("vote")

        request.data._mutable = _mutable
        serializer = ArticleDetailSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()

            photos = request.FILES.getlist("photos")
            for photo in photos:
                photo_name = default_storage.save(
                    os.path.join(
                        "article_photos",
                        str(serializer.instance.id),
                        photo.name.lower(),
                    ),
                    photo,
                )
                article_photo = ArticlePhoto(
                    article=serializer.instance, photo=photo_name
                )
                article_photo.save()
            if vote is not None and vote[0] != "":
                article_vote = ArticleVote(article=serializer.instance)
                article_vote.save()
                for item in vote:
                    if item == "":
                        continue
                    vote_item = ArticleVoteItem(vote=article_vote, title=item)
                    vote_item.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request, article_id):
        queryset = get_object_or_404(Article, pk=article_id)
        if queryset.is_deleted:
            raise exceptions.NotFound()
        serializer = ArticleDetailSerializer(queryset, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if (article.author != request.user) and (not request.user.is_staff):
            raise exceptions.PermissionDenied()
        article.is_deleted = True
        article.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, requset, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if (article.author != requset.user) and (not requset.user.is_staff):
            raise exceptions.PermissionDenied()
        serializer = ArticleDetailSerializer(
            article, data=requset.data, partial=True, context={"request": requset}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleLikeView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def post(self, requset, article_id):
        article = get_object_or_404(Article, pk=article_id)
        is_liked = article.is_like_user(requset.user)
        if is_liked:
            article.like_user_remove(requset.user)
        else:
            article.like_user_add(requset.user)
        like_count = article.like_count
        return JsonResponse({"is_liked": not is_liked, "like_count": like_count})


class Vote(APIView):
    permissions_classes = permissions.IsAuthenticated

    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        vote = get_object_or_404(ArticleVote, article=article)
        votes = ArticleVoteItem.objects.filter(vote=vote).all()
        vote_index = request.data.get("vote_index")
        voted_item = None
        for index, item in enumerate(votes):
            if item.voted_users.filter(pk=request.user.pk).exists():
                voted_item = index
                break
        if voted_item == vote_index:
            votes[voted_item].cancel_vote(request.user)
        else:
            if voted_item is not None:
                votes[voted_item].cancel_vote(request.user)
            votes[vote_index].do_vote(request.user)
        vote = votes[vote_index].vote
        return Response(ArticleVoteSerializer(vote, context={"request": request}).data)


class CommentView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def get(self, request, article_id):
        queryset = Comment.objects.filter(
            article__id=article_id, is_deleted=False
        ).order_by("id")
        serializers = CommentSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializers.data)

    def post(self, request, article_id):
        request.data.update({"article": article_id})

        article = get_object_or_404(Article, pk=article_id)
        if article.board.type == "ANON":
            request.data.update({"is_anonymous": True})
        elif article.board.type == "REAL":
            request.data.update({"is_anonymous": False})

        # Get Anonymous User Number
        anonymous_number = -1
        if request.data.get("is_anonymous") is True:
            if article.author == request.user:
                anonymous_number = 0
            else:
                prev_anon_comment = Comment.objects.filter(
                    article=article, author=request.user, is_anonymous=True
                )
                if prev_anon_comment.exists():
                    anonymous_number = prev_anon_comment.first().anonymous_number
                else:
                    biggest_anon_comment = Comment.objects.filter(
                        article=article, is_anonymous=True
                    ).order_by("-anonymous_number")
                    if biggest_anon_comment.exists():
                        anonymous_number = (
                            biggest_anon_comment.first().anonymous_number + 1
                        )
                    else:
                        anonymous_number = 1

        request.data.update({"anonymous_number": anonymous_number})

        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            article.comment_count += 1
            article.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDeleteView(APIView):
    permissions_classes = permissions.IsAuthenticated
    # post reply
    def post(self, request, comment_id):
        request.data.update({"comment": comment_id})
        serializer = ReplySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            comment = get_object_or_404(Comment, pk=comment_id)
            article = comment.article
            article.comment_count += 1
            article.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete, patch comment
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if (comment.author != request.user) and (not request.user.is_staff):
            raise exceptions.PermissionDenied()
        comment.is_deleted = True
        comment.article.comment_count -= 1
        comment.article.save()
        comment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, requset, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if (comment.author != requset.user) and (not requset.user.is_staff):
            raise exceptions.PermissionDenied()
        serializer = CommentSerializer(
            comment, data=requset.data, partial=True, context={"request": requset}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentLikeView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def post(self, requset, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        is_liked = comment.is_like_user(requset.user)
        if is_liked:
            comment.like_user_remove(requset.user)
        else:
            comment.like_user_add(requset.user)
        like_count = comment.like_count
        return JsonResponse({"is_liked": not is_liked, "like_count": like_count})


class ReplyUpdateDeleteView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def patch(self, request, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)
        if (reply.author != request.user) and (not request.user.is_staff):
            raise exceptions.PermissionDenied()
        serializer = ReplySerializer(
            reply, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requset, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)
        if (reply.author != requset.user) and (not requset.user.is_staff):
            raise exceptions.PermissionDenied()
        reply.is_deleted = True
        reply.comment.article.comment_count -= 1
        reply.comment.article.save()
        reply.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyLikeView(APIView):
    permissions_classes = permissions.IsAuthenticated

    def post(self, requset, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)
        is_liked = reply.is_like_user(requset.user)
        if is_liked:
            reply.like_user_remove(requset.user)
        else:
            reply.like_user_add(requset.user)
        like_count = reply.like_count
        return JsonResponse({"is_liked": not is_liked, "like_count": like_count})
