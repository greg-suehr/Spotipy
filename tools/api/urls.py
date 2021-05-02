# todo/api/urls.py : API urls.py
from django.conf.urls import url
from django.urls import path, include
from .views import (
    MyPlaylistsView,
)

urlpatterns = [
    path('', MyPlaylistsView.as_view()),
]
