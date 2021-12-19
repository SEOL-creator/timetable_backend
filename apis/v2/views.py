from django.http.response import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import FrontVersion
from ..serializers import FrontVersionSerializer


def frontVersionView(request):
    version = FrontVersion.objects.last().version
    return JsonResponse({"version": version})


class ReleaseNotesView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = FrontVersion.objects.all().order_by("-id")
        print(queryset[0].version)
        serializer = FrontVersionSerializer(queryset, many=True)
        return Response(serializer.data)
