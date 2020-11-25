from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post/', views.new_post, name='new_post'),
    path('<str:username>/', views.user_blog, name='user_blog'),
    path('follow/<str:username>/', views.follow, name='follow'),
]
