from django import forms

from .models import Mix, Comment

class UploadMixForm(forms.ModelForm):
    class Meta:
        model = Mix
        fields = ['mix_file', 'multitrack', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']