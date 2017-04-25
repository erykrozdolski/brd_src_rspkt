from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^$', views.index, name='main'),
    url(r'^administration/article_creator/(?P<idk>[0-9]+)?$', views.articleCreator, name='article_creator'),
    url(r'^administration/article_creator/ajax/$', views.articleCreatorOperations, name='article_creator_ajax'),
    url(r'^article_view/(?P<idk>[0-9]+)?/$', views.articleView, name='article_view'),
    url(r'^article_list/$', views.articleList, name='article_list'),
    url(r'^article_list/ajax/$', views.articleListOperations, name='article_list_ajax'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^section/(?P<section_name>)/$', views.sectionListView, name='section_view'),
    url(r'^section_list/$', views.sectionListView, name='section_list'),
    url(r'^test/$', views.test)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)