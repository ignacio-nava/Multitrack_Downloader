from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Tittle must be grater than 2 characters")]   
    )

    def __str__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Tittle must be grater than 2 characters")]   
    )
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    contact = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Multitrack(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Tittle must be grater than 2 characters")]   
    )
    preview = models.FileField(upload_to="previews/")
    number_channels = models.PositiveIntegerField(default=1)
    #content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    file_zip = models.FileField(upload_to="multitracks/")
    description = models.TextField()
    band = models.ForeignKey('Band', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title