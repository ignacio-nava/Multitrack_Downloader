from django.contrib import admin

from .models import Genre, Artist, Multitrack

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Multitrack)
