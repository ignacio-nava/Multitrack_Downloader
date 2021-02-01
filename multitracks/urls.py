from django.urls import path, reverse_lazy
from . import views

app_name = 'multitracks'
urlpatterns = [
    path('', views.MtListView.as_view(), name='all'),
    path('create', views.MtCreateView.as_view(success_url=reverse_lazy('multitracks:all')), name='mt_create'),
    path('mt/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='mt_favorite'),
    path('mt/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='mt_unfavorite'),
]