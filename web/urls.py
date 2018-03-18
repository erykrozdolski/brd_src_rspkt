from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from .views import account_views, administration_views, user_views

urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls'), name='tiny_mce'),
    url(r'^login/$', account_views.log_in, name='login'),
    url(r'^register/$', account_views.register, name='register'),
    url(r'^log_out/$', account_views.log_out, name='log_out'),
    url(r'^password_reminder/$', account_views.password_reminder, name='password_reminder'),
    url(r'^user_details/(?P<idk>[0-9]+)?/$', administration_views.userDetails, name='user_details'),
    url(r'^user_list/$', administration_views.usersList, name='users_list'),
    url(r'^$', user_views.index, name='index'),
    url(r'^administration/article_creator/(?P<idk>[0-9]+)?$', administration_views.articleCreator, name='article_creator'),
    url(r'^administration/article_creator/add/$', administration_views.add_article_component, name='add_article_component'),
    url(r'^administration/article_creator/edit/$', administration_views.edit_article_component, name='edit_article_component'),
    url(r'^administration/article_creator/delete/$', administration_views.delete_article_component, name='delete_article_component'),
    url(r'^article_details/(?P<idk>[0-9]+)?/$', administration_views.articleDetails, name='article_details'),
    url(r'^category_articles/(?P<idk>[0-9]+)?/$', user_views.category_articles, name='category_articles'),
    url(r'^category_details/(?P<idk>[0-9]+)?/$', administration_views.category_details, name='category_details'),
    url(r'^article_list/$', administration_views.articleList, name='article_list'),
    url(r'^article_list/ajax/$', administration_views.articleListAjax, name='article_list_ajax'),
    url(r'^category/$', administration_views.categoryList, name='category_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
