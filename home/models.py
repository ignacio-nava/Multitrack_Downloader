from django.db import models
from django.conf import settings

class SocialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='socialuser'
        )
    avatar_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username