from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=400)
    url = models.URLField(max_length=500)
    is_paying_user = models.BooleanField()
    has_video_in_staff_pick = models.BooleanField()
    has_atleast_one_video = models.BooleanField()

    class Meta:
        unique_together = ("name", "url")