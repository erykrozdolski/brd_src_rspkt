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

class ParagraphForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Component
        fields = ('header', 'text')
        widgets = {
            'header': TextInput(attrs={'class': 'width100','placeholder':"Tytuł jest używany tylko w trybie edycji"})
        }

class ParagraphForm(ModelForm):
    class Meta:
        model = Component
        fields = ('header',)
