from django.db import models
# from django.contrib.auth.models import User


class User(models.Model):
    uri  = models.CharField(max_length = 255, primary_key = True)
    name = models.CharField(max_length = 31) # Spotify's limit is 30
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}'s Library".format(self.username)


class Playlist(models.Model):
    uri  = models.CharField(max_length = 255, primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    created = models.DateTimeField()

    def __str__(self):
        return self.name

