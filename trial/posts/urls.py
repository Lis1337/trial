from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.user_blog, name='user_blog'),
    path('new_post/', views.new_post, name='new_post')
]
