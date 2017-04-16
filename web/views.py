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
    image_upload_form = ImageForm()
    quoteForm = QuoteForm()
    videoForm = VideoForm()
    paragraphForm = ParagraphForm()
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

            # Component.objects.update(manytomany=None).delete()
            article_form = ArticleForm(instance=article)
    else:
        article_form = ArticleForm(instance=article)

    return render(request, 'article/article_creator.html', {'article_form': article_form,
                                                            'article': article,
                                                            'idk': article.id,
                                                            'image_upload_form': image_upload_form,
                                                            'videoForm': videoForm,
                                                            'paragraphForm': paragraphForm,
                                                            'quoteForm': quoteForm})

def articleCreatorOperations(request):
    if request.POST.get('cmd', '') == 'addImage':
        component_form = ImageForm(data=request.POST, files=request.FILES, initial={'kind': 'image'})
    elif request.POST.get('cmd', '') == 'addParagraph':
        component_form = ParagraphForm(data=request.POST, initial={'kind': 'text'})
    elif request.POST.get('cmd', '') == 'addQuote':
        component_form = QuoteForm(data=request.POST, initial={'kind': 'quote'})
    elif request.POST.get('cmd', '') == 'addVideo':
        component_form = VideoForm(data=request.POST, initial={'kind': 'video'})
    if component_form.is_valid():
        component = component_form.save()
        idk = component.id
        response_data = {'success': True, 'idk': idk}
    else:
        print(component_form.errors)
        response_data = {'success': False}

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def articleView(request, idk=None):
    article = get_object_or_404(Article, pk=idk)
    if article.components:
        components = article.components.all().order_by('position')

    return render(request, 'article/article.html', {'article': article, 'components': components})


def articlesList(request):
    articleTable = ArticleTable(Article.objects.all())
    RequestConfig(request).configure(articleTable)

    return render(request, 'article/article_list.html', {'articleTable': articleTable})


def sectionListView(request):
    sectionListTable = SectionListTable(Section.objects.all())
    RequestConfig(request).configure(sectionListTable)
    return render(request, 'section.html', {'sectionListTable': sectionListTable})


def administration(request):
    return render(request, 'administration.html', {})

def test(request):
    return render(request, 'test.html', {})

