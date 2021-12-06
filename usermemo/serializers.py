from rest_framework import serializers
from rest_framework.fields import IntegerField
from accounts.serializers import UserSerializer
from .models import *


class ToDoListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ToDoList
        read_only_fields = ("created_at",)
        fields = ("id", "title", "description", "created_at", "completed", "author")

    def create(self, validated_data):
        todolist = ToDoList(
            title=validated_data["title"],
            description=validated_data["description"],
            author=self.context["request"].user,
        )
        todolist.save()
        return todolist


class ToDoListCommentSerializer(serializers.ModelSerializer):
    todolist = IntegerField(write_only=True, required=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = ToDoListComment
        read_only_fields = ("created_at",)
        write_only_fields = ("todolist",)
        fields = ("id", "author", "todolist", "comment", "created_at")

    def create(self, validated_data):
        comment = ToDoListComment(
            todolist_id=validated_data["todolist"],
            author=self.context["request"].user,
            comment=validated_data["comment"],
        )
        comment.save()
        return comment
