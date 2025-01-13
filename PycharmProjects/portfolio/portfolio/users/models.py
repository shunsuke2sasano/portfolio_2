from django.conf import settings
from django.db import models
from portfolio.portfolio.models import TimestampedModel

class UserProfile(TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 修正箇所
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    name = models.CharField(max_length=25)
    furigana = models.CharField(max_length=25)
    gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')])
    age = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return self.user.email

