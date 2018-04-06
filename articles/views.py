from django.shortcuts import render
from django.http import Http404
from .models import Article, Scientist, Topic, Tag


# Create your views here.

def tag_and_name_search(request, articles):
        receive_tags = request.POST.copy()
        receive_name = receive_tags['name']
        del receive_tags['name']
        copy_articles = list(articles[:])
        for article in list(articles):
            k = 0
            for tag in receive_tags.values():
                if tag in article.tags.values_list('name', flat=True):
                    k = 1
            if article.name == receive_name:
                k = 1
            if k == 0:
                copy_articles.remove(article)              
        return copy_articles 

def merge_articles_and_scientists():
        try:
            articles = list(Article.objects.order_by('-pub_date'))
            scientists = list(Scientist.objects.order_by('-pub_date'))
        except Article.DoesNotExist:
            Http404('Articles do not exists')
        except Scientist.DoesNotExist:
            Http404('Scientists do not exists')
        articles_and_scientists = articles[:]
        copy_scientists = scientists[:]
        k = 0
        for article in articles:
            for scientist in scientists:
                if article.pub_date < scientist.pub_date and scientist in copy_scientists:
                    articles_and_scientists.insert(articles.index(article)+k, scientist)
                    k +=1
                    copy_scientists.remove(scientist)
        if len(copy_scientists) > 0:
            for scientist in copy_scientists:
                articles_and_scientists.append(scientist)
        return articles_and_scientists
                
def sort_article_by_date(request, article_type, tag_id=0):
    if article_type == 'exercise' or article_type == 'theory':
        try:
            articles = Article.objects.filter(exerciese_or_theory=article_type).order_by('-pub_date')
        except Article.DoesNotExist:
            Http404('articles does not exists')
        if request.method == 'GET':
            return articles
        elif request.method == 'POST':
            return tag_and_name_search(request, articles)
    elif article_type == 'scientist':
        try:
            articles = Scientist.objects.order_by('-pub_date')
        except Scientist.DoesNotExist:
            Http404('scientists does not exists')
        if request.method == 'GET':
            return articles
        elif request.method == 'POST':
            return tag_and_name_search(request, articles)
    elif article_type == 'all':
        articles_and_scientists = merge_articles_and_scientists() 
        if request.method == 'GET':
            return articles_and_scientists
        elif request.method == 'POST':
            return tag_and_name_search(request, articles_and_scientists)
    elif article_type == 'tags':
        articles_and_scientists = merge_articles_and_scientists()
        art_and_sci = []
        for article in articles_and_scientists:
            for tag in article.tags.all():
                if tag.id == tag_id:
                    art_and_sci.append(article)
                    break;
        return art_and_sci

def pagination(n_articles,articles_id):
    articles_per_page = 4 
    full_pages = len(n_articles) // articles_per_page
    not_full_page = len(n_articles) % articles_per_page
    if not_full_page != 0:
            not_full_page = 1
    number_of_pages = full_pages + not_full_page;
    num_of_pages = [x for x in range(1,number_of_pages+1)]
    if articles_id == 0:
        n_articles_on_page = n_articles[0:4]
    else:
        n_articles_on_page = n_articles[4*(articles_id-1):4*(articles_id-1)+4]
    previous_page = articles_id-1
    next_page = articles_id+1
    long_previous_page = articles_id-5
    long_next_page = articles_id +5 
    if previous_page < 1:
        previous_page = 1
    if next_page > number_of_pages:
        next_page = number_of_pages
    if long_previous_page < 1:
        long_previous_page = 1
    if long_next_page > number_of_pages:
        long_next_page = number_of_pages
    result = {
            'previous_page': previous_page,
            'next_page': next_page,
            'long_previous_page': long_previous_page,
            'long_next_page': long_next_page,
            'number_of_pages': num_of_pages,
            'articles': n_articles_on_page, 
        }
    return result
                    
def index(request, articles_id):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Topics does not exists")
    n_articles = sort_article_by_date(request, 'all')
    
    result = pagination(n_articles,articles_id)
        
    context = {
        'tags': tags,
        'articles': result['articles'],
        'number_of_pages': result['number_of_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'long_previous_page': result['long_previous_page'],
        'long_next_page': result['long_next_page'],
        'type_i_or_t': 'index',
        
    }
    
    return render(request, 'articles/index.html', context)
   
def exercise(request, articles_id):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Topics does not exists")
    n_articles = sort_article_by_date(request, 'exercise')


    result = pagination(n_articles,articles_id)
    
    context = {
        'tags': tags,
        'articles': result['articles'],
        'number_of_pages': result['number_of_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'long_previous_page': result['long_previous_page'],
        'long_next_page': result['long_next_page'],
        'type': 'exercise',
    }
    
    return render(request, 'articles/exercises_or_theories.html', context)

def exercise_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)

def theories(request, articles_id):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Topics does not exists")
    n_articles = sort_article_by_date(request,'theory')

    result = pagination(n_articles,articles_id)
    
    context = {
        'tags': tags,
        'articles': result['articles'],
        'number_of_pages': result['number_of_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'long_previous_page': result['long_previous_page'],
        'long_next_page': result['long_next_page'],
        'type': 'theory',
    }
    return render(request, 'articles/exercises_or_theories.html', context)

def theories_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)

def scientists(request, articles_id):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Topics does not exists")
    n_scientists = sort_article_by_date(request, 'scientist')

    result = pagination(n_scientists,articles_id)
    
    context = {
        'tags': tags,
        'scientists': result['articles'],
        'number_of_pages': result['number_of_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'long_previous_page': result['long_previous_page'],
        'long_next_page': result['long_next_page'],
    }
    return render(request, 'articles/scientists.html', context)

def scientists_detail(request, scientist_id):
    scientist = Scientist.objects.get(id=scientist_id)
    context = {
        'scientist': scientist,
    }
    return render(request, 'articles/sientists_detail.html', context)

def topics(request):
    try:
        topics = Topic.get_annotated_list()
    except Topic.DoesNotExist:
        raise Htttp404("Topics does not exists")
    context = {
        'topics': topics,
    }
    return render(request, 'articles/topics.html', context)

def topic(request, topic_name, articles_id):

        articles = Article.objects.order_by('-pub_date')
        n_articles = list(articles[:])
        for article in articles:
            if article.topic.name != topic_name:
                n_articles.remove(article)

        result = pagination(n_articles,articles_id)
        
        context = {
            'topic_name':topic_name,
            'articles': result['articles'],
            'number_of_pages': result['number_of_pages'],
            'previous_page': result['previous_page'],
            'next_page': result['next_page'],
            'long_previous_page': result['long_previous_page'],
            'long_next_page': result['long_next_page'],
            'type_i_or_t': 'topic',
        }
        
        return render(request, 'articles/topic.html', context)

def tags(request, tag_id, articles_id):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Topics does not exists")
    n_articles = sort_article_by_date(request, 'tags', tag_id)

    result = pagination(n_articles,articles_id)
    
    context = {
        'tags': tags,
        'articles': result['articles'],
        'number_of_pages': result['number_of_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'long_previous_page': result['long_previous_page'],
        'long_next_page': result['long_next_page'],
        'type_i_or_t': 'tags',
        't_id': tag_id,
    }
    return render(request, 'articles/index.html', context)
