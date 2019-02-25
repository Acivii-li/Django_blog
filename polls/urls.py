#coding=utf-8
from django.urls import path
from django.contrib import admin

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/result/', views.ResultView.as_view(), name='result'),
    path('<int:question_id>/votes/', views.vote, name='vote'),
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
]