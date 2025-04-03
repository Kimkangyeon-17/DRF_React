from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings

# 상위 URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="", view=lambda request: redirect("/hottrack/")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
