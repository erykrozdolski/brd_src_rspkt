from django.forms import Form, DateField,ModelForm,FileInput, ModelChoiceField,MultipleChoiceField, ImageField, CharField, URLField, Form, ChoiceField, PasswordInput, FileField, Textarea, TextInput, Select
from .models import Article, Category, Component
from crispy_forms.helper import FormHelper

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    category = ModelChoiceField(label='kategoria', required=False, queryset=(Category.objects.all()))
    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            return title

    class Meta:
        model = Article
        widgets = {
            'cover': FileInput(attrs={'class': 'hidden', 'id': 'loadCover'}),
            'title': TextInput(attrs={'class': 'width100 form-control'}),
            'subtitle': TextInput(attrs={'class': 'width100 form-control'}),
            'tags': TextInput(attrs={'class': 'width100 form-control'}),
            'category': Select(attrs={'class': 'width100 form-control'}),
        }
        fields = ('title', 'subtitle', 'cover', 'category')

        labels = {'title': 'tytuł',
                  'subtitle': 'podtytuł',
                  'category': 'dział',
                  'cover': 'okładka',
                  'tags': 'tagi'}


class SearchArticleForm(Form):
    def __init__(self, *args, **kwargs):
        super(SearchArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['category'].choices = [(c.pk, c.name) for c in Category.objects.all()]

    category = MultipleChoiceField(label='kategoria', required=False, choices=[])
    title = CharField(label='tytuł', required=False)
    author = ChoiceField(label='autor', required=False)
    subtitle = CharField(label='podtytuł', required=False)
    published = ChoiceField(label='opublikowany', required=False)
    is_published = DateField(label='data publikacji', required=False)
    created = DateField(label='data utworzenia', required=False)
    search = CharField(label='', widget=TextInput(attrs={'placeholder': 'wyszukaj po frazie'}))


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Component
        fields = ('image', 'header', 'kind')
        widgets = {
            'image': FileInput(attrs={'class': 'hidden', 'id': 'changeImage'}),
            'header': TextInput(attrs={'class': 'width100 form-control', 'placeholder': "Tytuł jest używany tylko w trybie edycji"})
        }
        labels = {'header': 'tytuł grafiki',
                  'image': ''}


class ParagraphForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParagraphForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'text', 'kind')
        widgets = {
            'header': TextInput(attrs={'class': 'width100 form-control','placeholder':"Tytuł jest używany tylko w trybie edycji"}),
            'text': Textarea(attrs={'placeholder':'Dodaj treść kolumny','id': 'id_text'})
        }
        labels = {'header': 'tytuł akapitu',
                  'text': 'treść akapitu'}



class QuoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'quote', 'kind')
        widgets = {
            'header': TextInput(attrs={'class': 'width100 form-control','placeholder': "Tytuł jest używany tylko w trybie edycji"}),
            'quote': TextInput(attrs={'placeholder': 'Dodaj treść cytatu', 'id': 'id_quote', 'class': 'width100 form-control'}),
        }
        labels = {'header': 'tytuł cytatu',
                  'quote': 'treść cytatu'}


class VideoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'url', 'kind')
        widgets = {
            'header': TextInput(attrs={'class': 'width100 form-control','placeholder':"Tytuł jest używany tylko w trybie edycji"}),
            'url': TextInput(attrs={'placeholder': 'Dodaj adres URL', 'id': 'id_url', 'class': 'width100'})
        }
        labels = {'header': 'tytuł video',
                  'url': 'adres URL'}


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = ['name', 'cover']
        widgets = {
            # 'cover': FileInput(attrs={'class': 'hidden', 'id': 'loadCover'}),
            'name': TextInput(attrs={'class': 'width100 form-control'})
        }
        labels = {
            'name': 'nazwa działu'
        }


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
