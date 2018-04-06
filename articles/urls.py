from django.urls import path
from . import views
from .models import Article

app_name = 'articles'
urlpatterns = [    
    path('<int:articles_id>/', views.index, name='index'),
    path('exercise/<int:article_id>/', views.exercise_detail, name='exercise_detail'),
    path('theory/<int:article_id>/', views.theories_detail, name='theories_detail'),
    path('scientist/<int:scientist_id>/', views.scientists_detail, name='scientists_detail'),
    path('exercises/<int:articles_id>', views.exercise, name='exercises'),
    path('theories/<int:articles_id>', views.theories, name='theories'),
    path('scientists/<int:articles_id>', views.scientists, name='scientists'),
    path('topics/', views.topics, name='topics'),
    path('topic/<str:topic_name>/<int:articles_id>/', views.topic, name='topic'),
    path('tags/<int:tag_id>/<int:articles_id>/', views.tags, name='tags'),
    
]
