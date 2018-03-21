from django.urls import path
from . import views
from .models import Article
urlpatterns = [    
    path('', views.index, name='index'),
    path('exercises/<int:article_id>/', views.exercise_detail, name='exercise'),
    path('theories/<int:article_id>/', views.theories_detail, name='theories'),
    path('scientists/<int:scientist_id>/', views.scientists_detail, name='scientists'),
    path('exercises/', views.exercise, name='exercise'),
    path('theories/', views.theories, name='theories'),
    path('scientists/', views.scientists, name='scientists'),
    path('topics/', views.topics, name='topic'),
    
]
