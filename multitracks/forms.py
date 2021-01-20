from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Genre, Band, Multitrack

class CreateForm(forms.ModelForm):

    # preview = forms.FileField(required=False)

    class Meta:
        model = Multitrack
        fields = ['title', 'number_channels', 'description', 'preview']