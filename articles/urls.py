from django.urls import path
from . import views
from .models import Article

app_name = 'articles'
urlpatterns = [    
    path('', views.index, name='index'),
    path('exercise/<int:article_id>/', views.exercise_detail, name='exercise_detail'),
    path('theory/<int:article_id>/', views.theories_detail, name='theories_detail'),
    path('scientist/<int:scientist_id>/', views.scientists_detail, name='scientists_detail'),
    path('exercises', views.exercise, name='exercises'),
    path('theories', views.theories, name='theories'),
    path('scientists', views.scientists, name='scientists'),
    path('topics/', views.topics, name='topics'),
    path('topic/<str:topic_name>', views.topic, name='topic'),
    path('search/', views.search, name='search'),
    
]
