from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Scientist, Topic
from django.template import loader

# Create your views here.
def exercise_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return HttpResponse(article.text)

def theories_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return HttpResponse(article.text)

def scientists_detail(request, scientist_id):
    response = "You're looking at theory %s."
    return HttpResponse(response % scientist_id)

def exercise(request):
    all_exercise_articles = Article.objects.filter(exerciese_or_theory='exercise')
    all_exercise_articles_ordered = all_exercise_articles.order_by('-pub_date')
    return HttpResponse([a.text for a in all_exercise_articles_ordered])

def theories(request):
    all_exercise_articles = Article.objects.filter(exerciese_or_theory='theory')
    all_exercise_articles_ordered = all_exercise_articles.order_by('-pub_date')
    return HttpResponse([a.text for a in all_exercise_articles_ordered])

def scientists(request):
    all_scientists = Scientist.objects.order_by('-pub_date')
    return HttpResponse(scientist.text for scientist in all_scientists)

def topics(request):
    topics = Topic.objects.all()
    template = loader.get_template('articles/topics.html')
    context = {
        'topics': topics,    
    }
    return HttpResponse(template.render(context, request))

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

