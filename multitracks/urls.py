from django.urls import path, reverse_lazy
from . import views

app_name = 'multitracks'
urlpatterns = [
    path('', views.MtListView.as_view(), name='all'),
    path('create', views.MtCreateView.as_view(success_url=reverse_lazy('multitracks:all')), name='mt_create'),
    #path('preview/<int:pk>', views.stream_file, name='mt_preview'),
]