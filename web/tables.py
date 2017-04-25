from .models import Article, Section
import django_tables2 as tables
from django_tables2.utils import A

from django.utils.safestring import mark_safe
from django.utils.html import escape


class ImageColumn(tables.LinkColumn):
    def render(self, value):
        return mark_safe('<img class="thumbnail" src="/media/{}"/>'.format(escape(value)))


class ArticleTable(tables.Table):
    cover = ImageColumn(A('cover'))
    title = tables.LinkColumn('article_view', args=[A('pk')])
    akcje = tables.TemplateColumn(template_name='actions.html')
    class Meta:
        attrs = {'class': 'table'}
        exclude = ('tags', 'id')
        sequence = ('cover', 'title', 'subtitle')
        model = Article
        empty_text = "Na ten moment nie dodano żadnych artykułów"


class SectionListTable(tables.Table):
    class Meta:
        attr = {'class': 'table'}
        exclude = ('id',)
        model = Section
