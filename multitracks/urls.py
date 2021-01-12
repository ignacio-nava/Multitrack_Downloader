from django.urls import path
from . import views

app_name = 'multitracks'
urlpatterns = [
    path('', views.MtListView.as_view(), name='all')
]