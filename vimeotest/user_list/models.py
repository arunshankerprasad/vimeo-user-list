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

    def __unicode__(self):
        return u"""Name: {u.name}\n
        URL: {u.url}\n
        is_paying_user: {u.is_paying_user}\n
        has_video_in_staff_pick: {u.has_video_in_staff_pick}\n
        has_atleast_one_video: {u.has_atleast_one_video}""".format(u=self)


class UserFile(models.Model):
    user_file = models.FileField(upload_to='uploads/%Y/%m/%d')
    absolute_path = models.CharField(max_length=400)
    content_type = models.CharField(max_length=400)

