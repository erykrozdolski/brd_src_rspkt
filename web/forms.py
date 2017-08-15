from django.forms import Form, DateField,ModelForm,FileInput, ModelChoiceField, ImageField, CharField, URLField, Form, ChoiceField, PasswordInput, FileField, Textarea, TextInput, Select
from .models import Article, Category, Component
from crispy_forms.helper import FormHelper

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

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
            'category': Select(attrs={'class': 'width100 form-control'}, choices=Category.objects.all()),
        }
        fields = ('title', 'subtitle', 'category','cover')

        labels = {'title': 'tytuł',
                  'subtitle': 'podtytuł',
                  'category': 'dział',
                  'cover': 'okładka',
                  'tags': 'tagi'}


class SearchArticleForm(Form):
    def __init__(self, *args, **kwargs):
        super(SearchArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


    title = CharField(label='tytuł',required=False)
    author = CharField(label='autor',required=False)
    subtitle = CharField(label='podtytuł',required=False)
    published = ChoiceField(label='opublikowany',required=False)
    is_published = DateField(label='data publikacji',required=False)
    created = DateField(label='data utworzenia',required=False)
    category = ChoiceField(label='kategoria',required=False)

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
                  'image': '<button class="btn btn-default">wybierz obraz z dysku</button>'}


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
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'width100 form-control'})
        }
        labels = {
            'name': 'nazwa działu'
        }


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
