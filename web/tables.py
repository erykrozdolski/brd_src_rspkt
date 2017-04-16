from .models import Article, Section
import django_tables2 as tables


class ActionColumn(tables.Column):
    def render(self, value):
        return value.upper()


class ArticleTable(tables.Table):
    class Meta:
        attrs = {'class': 'table'}
        exclude = ('id',)
        model = Article


class SectionListTable(tables.Table):
    class Meta:
        attr = {'class': 'table'}
        exclude = ('id',)
        model = Section
