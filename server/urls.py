"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, re_path, include
from django.shortcuts import render
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token-auth/', obtain_jwt_token),
    path('tools/', include('tools.urls')),
]
