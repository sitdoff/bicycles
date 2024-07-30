from django.urls import include, path, re_path

urlpatterns = [
    re_path("", include("djoser.urls")),
    re_path("", include("djoser.urls.jwt")),
]
