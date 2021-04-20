# todo/api/urls.py : API urls.py
from django.conf.urls import url
from django.urls import path, include
from .views import (
    LibraryApiView,
)

urlpatterns = [
    path('', LibraryApiView.as_view()),
]
