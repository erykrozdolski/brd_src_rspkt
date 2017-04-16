from django.forms import ModelForm, ModelChoiceField, ImageField, CharField, URLField, Form, PasswordInput, FileField, Textarea, TextInput, Select
from .models import Article, Section, Component
from crispy_forms.helper import FormHelper

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.section = ModelChoiceField(queryset=Section.objects.all(), label="dział")

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            return title

    class Meta:
        model = Article
        widgets = {
            'title': TextInput(attrs={'class': 'width100'}),
            'subtitle': TextInput(attrs={'class': 'width100'}),
            'tags': TextInput(attrs={'class': 'width100'}),
            'section': Select(attrs={'class': 'width100'})
        }
        fields = ('title', 'subtitle', 'tags', 'section','cover')

        labels = {'title': 'tytuł',
                  'subtitle': 'podtytuł',
                  'section': 'dział',
                  'cover': 'okładka',
                  'tags': 'tagi'}


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('image', 'header')
        widgets = {
            'header': TextInput(attrs={'class': 'width100','placeholder':"Tytuł jest używany tylko w trybie edycji"})
        }
        labels = {'header': 'tytuł grafiki',
                  'image': ''}

class ParagraphForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParagraphForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'text')
        widgets = {
            'header': TextInput(attrs={'class': 'width100','placeholder':"Tytuł jest używany tylko w trybie edycji"}),
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
            'header': TextInput(attrs={'class': 'width100','placeholder': "Tytuł jest używany tylko w trybie edycji"}),
            'quote': TextInput(attrs={'placeholder': 'Dodaj treść cytatu', 'id': 'id_quote', 'class': 'width100'}),
            'kind': TextInput(attrs={'class':'hidden'})
        }
        labels = {'header': 'tytuł cytatu',
                  'quote': 'treść cytatu'}


class VideoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'url')
        widgets = {
            'header': TextInput(attrs={'class': 'width100','placeholder':"Tytuł jest używany tylko w trybie edycji"}),
            'url': TextInput(attrs={'placeholder': 'Dodaj adres URL', 'id': 'id_video', 'class': 'width100'})
        }
        labels = {'header': 'tytuł video',
                  'url': 'adres URL'}
