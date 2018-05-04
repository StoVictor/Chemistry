from django.shortcuts import render
from django.http import Http404
from .models import Article, Scientist, Topic, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    articles = []
    history = []

    try:
        articles = list(Article.objects.order_by('-pub_date'))
        history = list(Scientist.objects.order_by('-pub_date'))
    except Article.DoesNotExist:
        Http404('Articles do not exists')

    return merge_two_articles_lists_by_date(articles, history)


def merge_articles_lists(article_type):
    articles = []
    history = []

    try:
        articles = list(Article.objects.filter(exerciese_or_theory=article_type).order_by('-pub_date'))
        history = list(Scientist.objects.order_by('-pub_date'))
    except Article.DoesNotExist:
        Http404('Articles do not exists')

    return merge_two_articles_lists_by_date(articles, history)


def merge_two_articles_lists_by_date(list1, list2):
    result_list = list1[:]
    copy_list2 = list2[:]
    k = 0

    for article in list1:
        for scientist in list2:
            if article.pub_date < scientist.pub_date and scientist in copy_list2:
                result_list.insert(list1.index(article)+k, scientist)
                k += 1
                copy_list2.remove(scientist)

    if len(result_list) > 0:
        for scientist in copy_list2:
            result_list.append(scientist)

    return result_list


def get_articles_by_types(method, request, selected_tags):
    if method == 'POST':
        if ('filter_theory' in selected_tags.keys()
                and 'filter_exercise' in selected_tags.keys()
                and 'filter_history' in selected_tags.keys()):
            request.session['filter_theory'] = True
            request.session['filter_exercise'] = True
            request.session['filter_history'] = True
            return merge_articles_and_scientists()
        elif ('filter_theory' not in selected_tags.keys()
                and 'filter_exercise' in selected_tags.keys()
                and 'filter_history' in selected_tags.keys()):
            request.session['filter_theory'] = False
            request.session['filter_exercise'] = True
            request.session['filter_history'] = True
            return merge_articles_lists('exercise')
        elif ('filter_theory' in selected_tags.keys()
                and 'filter_exercise' not in selected_tags.keys()
                and 'filter_history' in selected_tags.keys()):
            request.session['filter_theory'] = True
            request.session['filter_exercise'] = False
            request.session['filter_history'] = True
            return merge_articles_lists('theory') 
        elif ('filter_theory' in selected_tags.keys()
                and 'filter_exercise' in selected_tags.keys()
                and 'filter_history' not in selected_tags.keys()):
            request.session['filter_theory'] = True
            request.session['filter_exercise'] = True
            request.session['filter_history'] = False
            return Article.objects.order_by('-pub_date')
        elif ('filter_theory' not in selected_tags.keys()
                and 'filter_exercise' not in selected_tags.keys()
                and 'filter_history' in selected_tags.keys()):
            request.session['filter_theory'] = False
            request.session['filter_exercise'] = False
            request.session['filter_history'] = True
            return Scientist.objects.order_by('-pub_date')
        elif ('filter_theory' in selected_tags.keys()
                and 'filter_exercise' not in selected_tags.keys()
                and 'filter_history' not in selected_tags.keys()):
            request.session['filter_theory'] = True
            request.session['filter_exercise'] = False
            request.session['filter_history'] = False
            return Article.objects.filter(exerciese_or_theory='theory').order_by('-pub_date')
        elif ('filter_theory' not in selected_tags.keys()
                and 'filter_exercise' in selected_tags.keys()
                and 'filter_history' not in selected_tags.keys()):
            request.session['filter_theory'] = False
            request.session['filter_exercise'] = True
            request.session['filter_history'] = False
            return Article.objects.filter(exerciese_or_theory='exercise').order_by('-pub_date')  
        elif ('filter_theory' not in selected_tags.keys()
                and 'filter_exercise' not in selected_tags.keys()
                and 'filter_history' not in selected_tags.keys()):
            request.session['filter_theory'] = False
            request.session['filter_exercise'] = False
            request.session['filter_history'] = False
            return []
    elif method == 'GET':
        if (request.session['filter_theory'] is True
                and request.session['filter_exercise'] is True
                and request.session['filter_history'] is True):
                return merge_articles_and_scientists()
        elif (request.session['filter_theory'] is False
                and request.session['filter_exercise'] is True
                and request.session['filter_history'] is True):
            return merge_articles_lists('exercise')
        elif (request.session['filter_theory'] is True
                and request.session['filter_exercise'] is False
                and request.session['filter_history'] is True):
            return merge_articles_lists('theory')                 
        elif (request.session['filter_theory'] is True
                and request.session['filter_exercise'] is True
                and request.session['filter_history'] is False):
            return Article.objects.order_by('-pub_date')                
        elif (request.session['filter_theory'] is False
                and request.session['filter_exercise'] is False
                and request.session['filter_history'] is True):
            return Scientist.objects.order_by('-pub_date')                
        elif (request.session['filter_theory'] is True
                and request.session['filter_exercise'] is False
                and request.session['filter_history'] is False):
            return Article.objects.filter(exerciese_or_theory='theory').order_by('-pub_date')                
        elif (request.session['filter_theory'] is False
                and request.session['filter_exercise'] is True
                and request.session['filter_history'] is False):
            return Article.objects.filter(exerciese_or_theory='exercise').order_by('-pub_date')                 
        elif (request.session['filter_theory'] is False
                and request.session['filter_exercise'] is False
                and request.session['filter_history'] is False):
            return []


def simple_view(request, articles,  template, type_of_article=None):
    try:
        n_articles = articles
    except Tag.DoesNotExist:
        raise Http404("There are no articles")

    paginator = Paginator(n_articles, 4)
    page = request.GET.get('page')

    context = {
        'articles': paginator.get_page(page),
        'type': type_of_article,
    }
    return render(request, template, context)


def simple_view_detail(request, article, template):
    context = {'article': article}
    return render(request, template, context)


def index(request):
    return simple_view(request, merge_articles_and_scientists(), 'articles/index.html')


def exercise(request):
    return simple_view(request, Article.objects.filter(exerciese_or_theory='exercise').order_by('-pub_date'),
                       'articles/index.html', 'exercise')


def exercise_detail(request, article_id):
    return simple_view_detail(request, Article.objects.get(id=article_id), 'articles/detail.html')


def theories(request):
    return simple_view(request, Article.objects.filter(exerciese_or_theory='theory').order_by('-pub_date'),
                       'articles/index.html', 'theory')


def theories_detail(request, article_id):
    return simple_view_detail(request, Article.objects.get(id=article_id), 'articles/detail.html')


def scientists(request):
    return simple_view(request,  Scientist.objects.order_by('-pub_date'), 'articles/scientists.html')


def scientists_detail(request, scientist_id):
    return simple_view_detail(request, Scientist.objects.get(id=scientist_id), 'articles/scientists_detail.html')


def topics(request):
    return simple_view(request, Topic.get_annotated_list(), 'articles/topics.html')


def topic(request, topic_name):
        articles = Article.objects.order_by('-pub_date')
        n_articles = list(articles[:])

        for article in articles:
            if article.topic.name != topic_name:
                n_articles.remove(article)

        paginator = Paginator(n_articles, 4)
        page = request.GET.get('page')

        context = {
            'topic_name': topic_name,
            'articles': paginator.get_page(page),
            'type_i_or_t': 'topic',
        }
        
        return render(request, 'articles/index.html', context)


def search(request):
    checked_list = {}
    ch = []
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Tag does not exists")

    selected_tags = []
    n_articles = []

    if request.method == 'POST':
        selected_tags = request.POST.copy()
        del selected_tags['csrfmiddlewaretoken']
        searched_name = selected_tags['name']
        del selected_tags['name']
        # selected_tags consists not only tags, but tags and types of searched articles
        # Inside get_articles_by_types in request.session['articles_selected_types'] add a filters by types
        articles = get_articles_by_types('POST', request, selected_tags)
        request.session['articles_selected_types'] = []

        request.session['articles_tags'] = {}

        for k, v in selected_tags.items():
            if 'tag' in k:
                request.session['articles_tags'][k] = v
        
        request.session['articles_name'] = searched_name
        n_articles = tag_and_name_search(request, articles)

        checked_list['history'] = request.session['filter_history']
        checked_list['theory'] = request.session['filter_theory']
        checked_list['exercise'] = request.session['filter_exercise']

    elif request.method == 'GET':
        try:
            checked_list['history'] = request.session['filter_history']
        except KeyError:
            request.session['filter_history'] = True
        try:
            checked_list['theory'] = request.session['filter_theory']
        except KeyError:
            request.session['filter_exercise'] = True
        try:
            checked_list['exercise'] = request.session['filter_exercise']
        except KeyError:
            request.session['filter_exercise'] = True

        if not request.GET.get('page'):
            request.session['articles_tags'] = {}

            checked_list['history'] = request.session['filter_history'] = True
            checked_list['theory'] = request.session['filter_exercise'] = True
            checked_list['exercise'] = request.session['filter_exercise'] = True

        articles = get_articles_by_types('GET', request, selected_tags)
        n_articles = []

        if not request.GET.get('tag_name'):
        
            for article in articles:
                for tag in request.session['articles_tags'].values():
                    if tag in article.tags.values_list('name', flat=True):
                        n_articles.append(article)
                        break
                if article.name in request.session['articles_name']:
                    n_articles.append(article)
        else:
            for article in articles:
                for tag in article.tags.all():
                    if tag.name == request.GET.get('tag_name'):
                        n_articles.append(article)
                        request.session['articles_tags']['tag' + str(tag.id)] = tag.name
            
    paginator = Paginator(n_articles, 4)
    page = request.GET.get('page')

    checked_tags = list(request.session['articles_tags'].keys())
    
    context = {
        'tags': tags,
        'articles': paginator.get_page(page),
        'checked_list': checked_list,
        'checked_tags': checked_tags,
        'ch': ch,
    }
    
    return render(request, 'articles/search.html', context)
