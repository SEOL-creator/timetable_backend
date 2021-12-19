from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("apis/v2/", include("apis.v2.urls")),
    path("apis/", include("apis.urls")),
]

if settings.DEBUG:
    urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
    urlpatterns += (
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    )
