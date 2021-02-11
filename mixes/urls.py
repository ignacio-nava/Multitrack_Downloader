from django.urls import path

from . import views

app_name = 'mixes'
urlpatterns = [
    path('', views.MixListView.as_view(), name='all'),
    path('by/<slug:slug>/', views.MixListView.as_view(), name='search_by_key'),
    path('create/', views.MixCreateView.as_view(), name='mix_create'),
    path('mix/<int:pk>/update/', views.MixUpdateView.as_view(), name='mix_update'),
    path('mix/<int:pk>/delete/', views.MixDeleteView.as_view(), name='mix_delete'),
    path('mix/<int:pk>/detail/', views.MixDetailView.as_view(), name='mix_detail'),
    path('mix/<int:pk>/comment/', views.CommentCreateView.as_view(), name='mix_comment_create'),
    path('mix/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='mix_comment_update'),
    path('mix/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='mix_comment_delete'),
    path('<int:pk>-comments', views.TalkComments.as_view(), name='comments'),
]