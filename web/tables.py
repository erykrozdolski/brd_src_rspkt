from .models import Article, Section
import django_tables2 as tables
from django_tables2.utils import A
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from django.utils.html import escape


class ImageColumn(tables.LinkColumn):
    def render(self, value):
        tn = get_thumbnail(value, '100x100', crop='center', quality=99)
        return mark_safe('<img class="thumbnail" src="/media/{}"/>'.format(escape(tn)))


class ArticleTable(tables.Table):
    cover = ImageColumn(A('cover'))
    title = tables.LinkColumn('article_view', args=[A('pk')])
    akcje = tables.TemplateColumn(template_name='actions.html')
    checkbox = tables.CheckBoxColumn(verbose_name='', accessor='pk')
    class Meta:
        attrs = {'class': 'admin_table', 'id': "article_table"}
        exclude = ('tags', 'id')
        sequence = ('checkbox', 'cover', 'title', 'subtitle')
        model = Article
        empty_text = "Na ten moment nie dodano żadnych artykułów"


class SectionListTable(tables.Table):
    class Meta:
        attr = {'class': 'table'}
        exclude = ('id',)
        model = Section
        empty_text = "Na ten moment nie dodano żadnych działów"
