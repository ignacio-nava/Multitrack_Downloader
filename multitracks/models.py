from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class Multitrack(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Tittle must be grater than 2 characters")]   
    )
    #file
    #file_zip
    number_channels = models.PositiveIntegerField(default=1)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)