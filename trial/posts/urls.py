from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post/', views.new_post, name='new_post'),
    path('current_user_feed/', views.current_user_feed, name='current_user_feed'),
    path('current_user_feed/mark_as_read/<int:post_id>', views.mark_as_read, name='mark_as_read'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('<str:username>/', views.user_blog, name='user_blog'),
]
