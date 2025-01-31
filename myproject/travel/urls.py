from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('comment/like/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('comment/dislike/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('reset-clicks/', views.reset_clicks_on_login, name='reset_clicks'),  # Reset click count after login
]
