from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

from multitracks.models import Multitrack

class Mix(models.Model):
    multitrack = models.ForeignKey(Multitrack, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mix_file = models.FileField(upload_to="mixes/")
    description = models.TextField(null=True, blank=True)
    # Comments
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
               through='Comment', related_name='comments_owned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}'s mix"

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
        )
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'