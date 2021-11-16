from .models import User
from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname",)
        read_only_fields = ("id", "email")


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    nickname = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    code = serializers.CharField(required=False, write_only=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ("email", "nickname", "password", "password2", "code", "is_active")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"], nickname=validated_data["nickname"]
        )
        user.set_password(validated_data["password"])
        if validated_data["code"] == "j6sy5w":
            user.is_active = True
        user.save()

        return user
