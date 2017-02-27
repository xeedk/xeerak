from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url

from django.conf.urls.static import static
from plugins.native.views import NativeAPI

urlpatterns = [
    url(r'^', NativeAPI.as_view()),

]