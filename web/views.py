from django.shortcuts import render
from .forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm
from .handlers import *
from .models import Component, Article, Category
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,  JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.urlresolvers import reverse

def index(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'base.html', {'articles': articles})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnianie zakończyło się sukcesem')
                else:
                    return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def articleCreator(request, idk=None):
    if not idk:
        article = Article()
    else:
        article = get_object_or_404(Article, pk=idk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article, files=request.FILES)
        components_idks = request.POST.getlist('component_idk')
        position_index = request.POST.getlist('component_position')
        id_and_position = zip(components_idks, position_index)
        if article_form.is_valid():
            article = article_form.save()
            for idk, position in id_and_position:
                component = get_object_or_404(Component, pk=idk)
                component.position = position
                component.save()
                article.components.add(component)
                article.author = request.user
                article.save()
            return redirect(reverse('article_details', kwargs={'idk': article.id}))
        else:
            article_form = ArticleForm(instance=article, files=request.FILES)
    else:
        article_form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    return render(request, 'article/article_creator.html', {'article_form': article_form,
                                                            'article': article,
                                                            'idk': article.id,
                                                            'image_upload_form': ImageForm(),
                                                            'videoForm': VideoForm(),
                                                            'paragraphForm': ParagraphForm(),
                                                            'quoteForm': QuoteForm(),
                                                            })


def set_component_form(request, kind, component=None):
    if kind == 'image':
        form = ImageForm(instance=component, data=request.POST, files=request.FILES, initial={'kind': 'image'})
    elif kind == 'text':
        form = ParagraphForm(instance=component, data=request.POST, initial={'kind': 'text'})
    elif kind == 'quote':
        form = QuoteForm(instance=component, data=request.POST, initial={'kind': 'quote'})
    elif kind == 'url':
        form = VideoForm(instance=component, data=request.POST, initial={'kind': 'url'})
    else:
        raise AttributeError
    return form



def add_article_component(request):
    response_data = {'success': False}
    if request.POST:
        kind = request.POST.get('kind')
        component_form = set_component_form(request, kind)
        if component_form.is_valid():
            component = component_form.save()
            idk = component.id
            kind = component.get_kind_display()
            response_data = {'success': True, 'idk': idk, 'kind': kind}

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def edit_article_component(request):
    response_data = {'success': False}
    if request.POST:
        idk = request.POST.get('idk', '')
        cmd = request.POST.get('cmd', '')
        if cmd == 'before_edit':
            component = get_object_or_404(Component, pk=idk)
            header = component.header
            if component.kind == 'image':
                component_data = ''
            else:
                component_data = getattr(component, component.kind)
            modal = '#edit{}Modal'.format(component.kind.capitalize())
            input_el = '#id_{}'.format(component.kind)
            response_data = {'success': True, 'header': header, 'modal': modal, 'component_data': component_data,
                             'input_el': input_el}
        else:
            kind = request.POST.get('kind')
            component = get_object_or_404(Component, pk=idk)
            component_form = set_component_form(request, kind, component)
            if component_form.is_valid():
                component_form.save()
                response_data = {'success': True}
            else:
                response_data = {'success': False}

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def delete_article_component(request):
    response_data = {'success': False}
    if request.POST:
        idk = request.POST.get('idk', '')
        if idk:
            component = get_object_or_404(Component, pk=idk)
            component.delete()
            response_data = {'success': True}

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def articleDetails(request, idk=None):
    article = get_object_or_404(Article, pk=idk)
    articles = Article.objects.all()
    if article.components:
        components = article.components.all().order_by('position')

    return render(request, 'article/article.html', {'article': article,
                                                    'components': components,
                                                    'articles': articles,})


def articleList(request):
    from web.forms import SearchArticleForm
    article_list = Article.objects.all()
    search_form = SearchArticleForm()
    if request.is_ajax():
        response_data = {}
        cmd = request.POST.get('cmd', '')
        idk = request.POST.get('idk', '')
        article = get_object_or_404(Article, pk=idk)
        if cmd == 'delete_article':
            article.delete()
            response_data = {'success': True}
        elif cmd == 'publish_article':
            article.publish()
            response_data = {'success': True}
        elif cmd == 'unpublish_article':
            article.unpublish()
            response_data = {'success': True}
        return JsonResponse(response_data)
    return render(request, 'article/article_list.html', {'article_list': article_list,
                                                         'search_form': search_form})


def category_details(request, idk=None):
    if request.POST:
        category_form = CategoryForm(data=request.POST, files=request.FILES)
        if idk:
            category_form.instance = get_object_or_404(Category, pk=idk)
        if category_form.is_valid():
            category_form.save()
            return redirect('category_list')
    else:
        if idk:
            category_form = CategoryForm(instance=get_object_or_404(Category, pk=idk))
        else:
            category_form = CategoryForm()
    return render(request, 'category/category_details.html', {'category_form': category_form})


def categoryList(request):
    category_form = CategoryForm()
    all_categories = Category.objects.all()
    if request.is_ajax():
        cmd = request.POST.get('cmd', '')
        if cmd == 'delete_category':
            category = get_object_or_404(Category, pk=request.POST.get('idk',''))
            category.delete()
            return render(request, 'category/category_results.html', {'category_list': all_categories})

    return render(request, 'category/category_list.html', {'category_form': category_form,
                                                  'category_list': all_categories
                                                  })


def articleListAjax(request):
    all_offers = Article.objects.all()
    filtered_articles = Article.objects.all()
    post_data = request.POST.dict()
    del post_data['csrfmiddlewaretoken']
    if 'search' in post_data:
        if post_data['search']:
            phrase = post_data['search']
            del post_data['search']
            filtered_articles = Article.objects.none()
            fields = ['title', 'subtitle']
            for field in fields:
                if field == 'category':
                    pass
                else:
                    qs = all_offers.filter(**{field + '__icontains': phrase})
                    filtered_articles = filtered_articles | qs
    for key in post_data:
        if key == 'category':
            values_list = request.POST.getlist(key)
            filtered_articles = filtered_articles.filter(**{key + '__in': values_list})
        elif post_data[key]:
            values_list = request.POST.getlist(key)
            filtered_articles = filtered_articles.filter(**{key + '__icontains': values_list})

    return render(request, 'article/article_results.html', {'article_list': filtered_articles.distinct()})
