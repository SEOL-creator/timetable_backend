from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import *
from school.models import School
from accounts.models import User


class BoardSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(), write_only=True
    )

    class Meta:
        model = Board
        fields = ("school", "title", "code", "type")

    def create(self, validated_data):
        board = Board(
            school=validated_data["school"],
            title=validated_data["title"],
            code=validated_data["code"],
        )
        board.save()
        return board


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()
    am_i_author = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.is_like_user(user)

    def get_author(self, obj):
        if obj.is_anonymous:
            return None
        else:
            return UserSerializer(obj.author).data

    def get_am_i_author(self, obj):
        user = self.context["request"].user
        return obj.author == user

    def get_board(self, obj):
        return BoardSerializer(obj.board).data

    class Meta:
        model = Article
        fields = (
            "id",
            "board",
            "title",
            "content",
            "author",
            "created_at",
            "is_updated",
            "is_liked",
            "like_count",
            "comment_count",
            "is_anonymous",
            "am_i_author",
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    am_i_author = serializers.SerializerMethodField()

    def get_comments(self, obj):
        queryset = Comment.objects.filter(article=obj, is_deleted=False)
        serializer = CommentSerializer(queryset, many=True, context=self.context)
        return serializer.data

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.is_like_user(user)

    def get_author(self, obj):
        if obj.is_anonymous:
            return None
        else:
            return UserSerializer(obj.author).data

    def get_am_i_author(self, obj):
        user = self.context["request"].user
        return obj.author == user

    class Meta:
        model = Article
        fields = (
            "id",
            "board",
            "title",
            "content",
            "author",
            "created_at",
            "is_updated",
            "is_liked",
            "like_count",
            "comment_count",
            "comments",
            "is_anonymous",
            "am_i_author",
        )

    def create(self, validated_data):
        article = Article(
            board=validated_data["board"],
            title=validated_data["title"],
            content=validated_data["content"],
            author=self.context["request"].user,
            is_anonymous=validated_data["is_anonymous"],
        )
        article.save()
        return article


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    replys = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), write_only=True
    )
    am_i_author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if obj.is_anonymous:
            return None
        else:
            return UserSerializer(obj.author).data

    def get_replys(self, obj):
        queryset = Reply.objects.filter(comment=obj, is_deleted=False)
        serializer = ReplySerializer(
            queryset, many=True, context={"request": self.context["request"]}
        )
        return serializer.data

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.is_like_user(user)

    def get_am_i_author(self, obj):
        user = self.context["request"].user
        return obj.author == user

    class Meta:
        model = Comment
        fields = (
            "id",
            "article",
            "author",
            "content",
            "created_at",
            "is_updated",
            "is_liked",
            "like_count",
            "replys",
            "is_anonymous",
            "anonymous_number",
            "am_i_author",
        )

    def create(self, validated_data):
        comment = Comment(
            article=validated_data["article"],
            author=self.context["request"].user,
            content=validated_data["content"],
            is_anonymous=validated_data["is_anonymous"],
            anonymous_number=validated_data["anonymous_number"],
        )
        comment.save()
        return comment


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    mentioned_user = serializers.SerializerMethodField(read_only=True)
    mentioned_user_id = serializers.IntegerField(
        write_only=True, required=False, default=None
    )
    is_liked = serializers.SerializerMethodField()
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), write_only=True
    )
    am_i_author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if obj.is_anonymous:
            return None
        else:
            return UserSerializer(obj.author).data

    def get_mentioned_user(self, obj):
        if obj.mention_user:
            return obj.mention_user.nickname
        return None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.is_like_user(user)

    def get_am_i_author(self, obj):
        user = self.context["request"].user
        return obj.author == user

    class Meta:
        model = Reply
        fields = (
            "id",
            "comment",
            "author",
            "mentioned_user",
            "mentioned_user_id",
            "content",
            "created_at",
            "is_updated",
            "is_liked",
            "like_count",
            "is_anonymous",
            "am_i_author",
        )

    def create(self, validated_data):
        reply = Reply(
            comment=validated_data["comment"],
            mention_user_id=validated_data["mentioned_user_id"],
            author=self.context["request"].user,
            content=validated_data["content"],
        )
        reply.save()
        return reply
