from django.urls import path

from . import views

app_name = 'mixes'
urlpatterns = [
    path('', views.mixList, name='all'),
]