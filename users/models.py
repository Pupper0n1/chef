from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    friends = models.ManyToManyField("Profile", blank=True, symmetrical=True)
    followers = models.ManyToManyField("Profile", blank=True, symmetrical=False)
    picture = models.ImageField(upload_to="profile_pic", blank=True)