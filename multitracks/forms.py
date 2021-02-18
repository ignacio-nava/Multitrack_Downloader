from django import forms
from .models import Multitrack

class CreateForm(forms.ModelForm):

    class Meta:
        model = Multitrack
        fields = ['title', 'number_channels', 'description', 'preview', 'file_zip', 'genre', 'artist']