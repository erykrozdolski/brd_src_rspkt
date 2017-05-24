from django.shortcuts import render
from .forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm
from .handlers import *
from .models import Component, Article, Section
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.urlresolvers import reverse
from .tables import ArticleTable, SectionListTable
from django_tables2 import RequestConfig
import pdb

def index(request):
    return render(request, 'base.html', {})


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
                article.save()
            return redirect(reverse('article_view', kwargs={'idk': article.id}))
        else:
            article_form = ArticleForm(instance=article)
    else:
        article_form = ArticleForm(instance=article)

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
                print(component_form.errors)
                response_data = {'success': False}
            print(component.text)

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


def articleView(request, idk=None):
    article = get_object_or_404(Article, pk=idk)
    if article.components:
        components = article.components.all().order_by('position')

    return render(request, 'article/article.html', {'article': article, 'components': components})


def articleList(request):
    articleTable = ArticleTable(Article.objects.all())
    RequestConfig(request).configure(articleTable)

    return render(request, 'article/article_list.html', {'articleTable': articleTable})


def articleListOperations(request):
    idk = request.POST.get('idk', '')
    if request.POST:
        article = get_object_or_404(Article, pk=idk)
        article.delete()

    response_data = {'success': True}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def sectionListView(request):
    sectionListTable = SectionListTable(Section.objects.all())
    return render(request, 'section.html', {'sectionListTable': sectionListTable})


def administration(request):
    return render(request, 'administration.html', {})

def test(request):
    return render(request, 'test.html', {})

