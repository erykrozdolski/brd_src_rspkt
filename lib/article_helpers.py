from django.shortcuts import render
from web.forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm, UserForm, EditUserForm, PasswordRemindForm
from web.handlers import *
from web.models import Component, Article, Category, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,  JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.urlresolvers import reverse


def set_component_form(request, kind, component=None):
    if kind == 'image':
        form = ImageForm(instance=component, data=request.POST, files=request.FILES, initial={'kind': 'image'})
    elif kind == 'text':
        form = ParagraphForm(instance=component, data=request.POST, initial={'kind': 'paragraph'})
    elif kind == 'quote':
        form = QuoteForm(instance=component, data=request.POST, initial={'kind': 'quote'})
    elif kind == 'url':
        form = VideoForm(instance=component, data=request.POST, initial={'kind': 'url'})
    else:
        raise AttributeError
    return form
