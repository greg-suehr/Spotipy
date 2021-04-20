from django.db import models
from django.contrib.auth.models import User

class Library(models.Model):
    username  = models.CharField(max_length = 32) # Spotify's limit is 30
    created   = models.DateTimeField(auto_now = True)
    updated   = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "{}'s Library".format(self.username)
    
