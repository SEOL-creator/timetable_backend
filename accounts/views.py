import json
import os
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from django.core.files.storage import default_storage
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, generics, exceptions, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import User

from .serializers import (
    DetailedUserSerializer,
    RegisterSerializer,
    UserSerializer,
)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return Response({"token": token.key, "user": DetailedUserSerializer(user).data})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


@csrf_exempt
def validateToken(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            token = Token.objects.get(key=data["token"])
            user = token.user
            serializer = DetailedUserSerializer(user)
            user_logged_in.send(sender=user.__class__, request=request, user=user)
        except Token.DoesNotExist:
            return JsonResponse({"valid": False}, status=200)
        return JsonResponse(
            {"valid": True, "user": serializer.data},
            status=200,
        )
    else:
        return JsonResponse(
            {"detail": f"""메소드(Method) "{request.method}"는 허용되지 않습니다."""}, status=405
        )


class UserListView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        queryset = User.objects.all().order_by("date_joined")
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, id):
        if id == "me":
            queryset = request.user
            serializer = DetailedUserSerializer(queryset)
        else:
            id = int(id)
            queryset = get_object_or_404(User, id=id)
            serializer = UserSerializer(queryset, read_only=True)
        return Response(serializer.data)

    def patch(self, request, id):
        user = get_object_or_404(User, id=int(id))
        if (request.user != user) and (not request.user.is_staff):
            raise exceptions.PermissionDenied()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def user_profile_pic_upload(request):
    user = request.user
    image = request.FILES["image"]
    image_name = default_storage.save(
        os.path.join("profilepic", str(user.id), image.name.lower()), image
    )
    user.profilepic = image_name
    user.save(update_fields=["profilepic"])
    serializer = UserSerializer(user)
    return Response(serializer.data)
