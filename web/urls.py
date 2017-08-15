from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^$', views.index, name='main'),
    url(r'^administration/article_creator/(?P<idk>[0-9]+)?$', views.articleCreator, name='article_creator'),
    url(r'^administration/article_creator/add/$', views.add_article_component, name='add_article_component'),
    url(r'^administration/article_creator/edit/$', views.edit_article_component, name='edit_article_component'),
    url(r'^administration/article_creator/delete/$', views.delete_article_component, name='delete_article_component'),
    url(r'^article_details/(?P<idk>[0-9]+)?/$', views.articleDetails, name='article_details'),
    url(r'^article_list/$', views.articleList, name='article_list'),
    url(r'^article_list/ajax/$', views.articleListAjax, name='article_list_ajax'),
    url(r'^category/$', views.categoryList, name='category_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



