from django.forms import ModelForm,FileInput, ModelChoiceField, ImageField, CharField, URLField, Form, PasswordInput, FileField, Textarea, TextInput, Select
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
            'cover': FileInput(attrs={'class': 'hidden', 'id': 'loadCover'}),
            'title': TextInput(attrs={'class': 'width100 form-control'}),
            'subtitle': TextInput(attrs={'class': 'width100 form-control'}),
            'tags': TextInput(attrs={'class': 'width100 form-control'}),
            'section': Select(attrs={'class': 'width100 form-control'}),
        }
        fields = ('title', 'subtitle', 'section','cover')

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


class SectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Section
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
