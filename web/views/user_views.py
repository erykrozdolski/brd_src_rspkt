from django.shortcuts import render
from web.forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm, UserForm, EditUserForm, PasswordRemindForm
from web.handlers import *
from web.models import Component, Article, Category, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,  JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.urlresolvers import reverse


def index(request):
    main_article = Article.get_main()
    popular_articles = Article.get_most_popular()
    newest_articles = Article.get_n_newest()
    categories = Category.objects.all()
    return render(request, 'base_content.html', {'main_article': main_article,
                                                 'popular_articles': popular_articles,
                                                 'newest_articles': newest_articles,
                                                 'categories': categories})


def category_articles(request, idk=None):
    articles = Article.objects.filter(category=get_object_or_404(Category, pk=idk))
    categories = Category.objects.all()

    return render(request, "category_view.html", {'articles': articles,
                                                  'categories':categories})
