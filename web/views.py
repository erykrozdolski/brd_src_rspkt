from django.shortcuts import render
from .forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm
from .handlers import *
from .models import Component, Article, Category
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.urlresolvers import reverse

def index(request):
    articles = Article.objects.all()[0:9]
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
    return render(request, 'article/article_list.html', {'article_list': article_list,
                                                         'search_form': search_form})


def articleListOperations(request):
    idk = request.POST.get('idk', '')
    if request.POST:
        article = get_object_or_404(Article, pk=idk)
        article.delete()

    response_data = {'success': True}
    return HttpResponse(json.dumps(response_data), content_type='application/json')




def categoryList(request):
    category_list = Category.objects.all()
    category_form = CategoryForm()
    if request.is_ajax():
        response_data = {'success': True}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    return render(request, 'category_list.html', {'category_form': category_form,
                                                 'category_list': category_list})


def articleListAjax(request):
    all_offers = Article.objects.all().exclude(jobTitle='staż/ praktyki')
    filtered_articles = Article.objects.all()
    post_data = request.POST.dict()
    del post_data['csrfmiddlewaretoken']
    if 'search' in post_data:
        if post_data['search']:
            phrase = post_data['search']
            del post_data['search']
            filtered_articles = Article.objects.none()
            fields = ['company_size',  'description', 'jobTitle', 'neighbourhood','category', 'benefits',
                      'remote_job', 'requirements', 'seniority_level', 'town', 'working_hours']
            for field in fields:
                qs = all_offers.filter(**{field + '__icontains': phrase})
                filtered_offers = filtered_offers | qs
    for key in post_data:
        if post_data[key]:
            values_list = request.POST.getlist(key)
            filtered_offers = filtered_offers.filter(**{key + '__in': values_list})

    return render(request, 'offers/article_results.html', {'article_list': filtered_articles.distinct()})
