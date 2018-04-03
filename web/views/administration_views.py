from django.shortcuts import render
from web.forms import ArticleForm, LoginForm, ImageForm, VideoForm, QuoteForm, ParagraphForm, CategoryForm, UserForm, EditUserForm, PasswordRemindForm
from web.handlers import *
from web.forms import SearchArticleForm
from web.models import Component, Article, Category, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,  JsonResponse
from django.shortcuts import get_object_or_404, redirect
from lib.article_helpers import set_component_form
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


@login_required
def add_article_component(request):
    response_data = {'success': False}
    if request.POST:
        kind = request.POST.get('kind')
        component_form = set_component_form(request, kind)
        if component_form.is_valid():
            component = component_form.save()
            print("Jest valid", component)
            idk = component.id
            kind = component.get_kind_display()
            response_data = {'success': True, 'idk': idk, 'kind': kind}

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
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
            print(component_data)
            tab = '#{}Tab'.format(component.kind)
            input_el = '#id_{}'.format(component.kind)
            response_data = {'success': True, 'header': header, 'tab': tab, 'component_data': component_data,
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


@login_required
def delete_article_component(request):
    response_data = {'success': False}
    if request.POST:
        idk = request.POST.get('idk', '')
        if idk:
            component = get_object_or_404(Component, pk=idk)
            component.delete()
            response_data = {'success': True}

    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def articleDetails(request, idk=None):
    article = get_object_or_404(Article, pk=idk)
    articles = Article.objects.all()[0:5]
    categories = Category.objects.all()
    popular_articles =  Article.get_most_popular()

    if article.components:
        components = article.components.all().order_by('position')

    return render(request, 'article/article.html', {'article': article,
                                                    'components': components,
                                                    'articles': articles,
                                                    'popular_articles': popular_articles,
                                                    'categories':categories})

@login_required
def articleList(request):
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
            article.save()
            response_data = {'success': True, 'pub_date': article.published}
        elif cmd == 'unpublish_article':
            article.unpublish()
            article.save()
            response_data = {'success': True, 'pub_date': '-'}
        return JsonResponse(response_data)
    return render(request, 'article/article_list.html', {'article_list': article_list,
                                                         'search_form': search_form})

@login_required
def category_details(request, idk=None):
    if idk:
        category = get_object_or_404(Category, pk=idk)
        category_form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
    else:
        category = Category()
        category_form = CategoryForm()
    if request.POST:
        category_form = CategoryForm(instance=category, data=request.POST, files=request.FILES)
        if category_form.is_valid():
            category_form.save()
            return redirect('category_list')



    return render(request, 'category/category_details.html', {'category_form': category_form})


@login_required
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

@login_required
def usersList(request):
    users_list = User.objects.all()
    if request.is_ajax():
        response_data = {'success': True}
        cmd = request.POST.get('cmd', '')
        user = get_object_or_404(User, pk=request.POST.get('idk', ''))
        if cmd == 'delete_user':
            user.delete()
        elif cmd == 'unblock_user':
            user.unblock()
            response_data = {'text': 'aktywny', 'button_label': 'Zablokuj', 'command': 'block_user'}

        elif cmd == 'block_user':
            user.block()
            response_data = {'text': 'zablokowany', 'button_label': 'Odblokuj', 'command': 'unblock_user'}


        return JsonResponse(response_data)
    return render(request, 'administration/users_list.html', {
                                                  'users_list': users_list
                                                  })

@login_required
def userDetails(request, idk=None):
    if request.POST:
        if idk:
            user_form = EditUserForm(data=request.POST, instance=get_object_or_404(User, pk=idk))
        else:
            user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('users_list')
    else:
        if idk:
            user_form = EditUserForm(instance=get_object_or_404(User, pk=idk))
        else:
            user_form = UserForm()

    return render(request, 'administration/user_details.html', {'user_form': user_form,
                                                                'idk': idk
                                                                })

@login_required
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


@login_required
def articleCreator(request, idk=None):
    if idk:
        article = get_object_or_404(Article, pk=idk)
    else:
        article = Article()
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
            return redirect(reverse('article_creator', kwargs={'idk': article.id}))
        else:
            article_form = ArticleForm(instance=article, files=request.FILES)
    else:
        if idk:
            article_form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
        else:
            article_form = ArticleForm()

    return render(request, 'article/article_creator.html', {'article_form': article_form,
                                                            'article': article,
                                                            'idk': article.id,
                                                            'image_upload_form': ImageForm(),
                                                            'videoForm': VideoForm(),
                                                            'paragraphForm': ParagraphForm(),
                                                            'quoteForm': QuoteForm(),
                                                            })
