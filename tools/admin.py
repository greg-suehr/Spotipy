from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Library)
admin.site.register(models.Playlist)
