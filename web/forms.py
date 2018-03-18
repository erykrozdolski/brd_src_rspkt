from django.forms import EmailField, ValidationError, Form, DateField,ModelForm,FileInput,ModelChoiceField,MultipleChoiceField, ImageField, CharField, URLField, Form, ChoiceField,PasswordInput, FileField, Textarea, TextInput, Select
from .models import Article, Category, Component, User
from crispy_forms.helper import FormHelper


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'bio', 'password', 'avatar']
        widgets = {
            'password': PasswordInput(),
            'avatar': FileInput(attrs={'class': 'hidden', 'id': 'add_image'}),

        }
        labels = {'username': 'nazwa użytkownika',
                  'first_name': 'imię',
                  'last_name': 'nazwisko',
                  'email': 'email',
                  'password': 'hasło',
                  }

    def clean_username(self):
        cleaned_data = super(UserForm, self).clean()
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Taki użytkownik już istnieje')
        else:

            return username

    def clean_email(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Użytkownik o takim adresie e-mail już istnieje')
        else:
            return email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        if not password or len(password) < 8:
            self.add_error('password', 'Hasło musi mieć przynajmniej 8 znaków')
        else:
            return cleaned_data


class EditUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar']
        labels = {'username': 'nazwa użytkownika',
                  'first_name': 'imię',
                  'last_name': 'nazwisko',
                  'email': 'email',
                  }

        widgets = {
            'avatar': FileInput(attrs={'class': 'hidden', 'id': 'add_image'}),
        }


class ArticleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['cover'].required = False

    category = ModelChoiceField(label='kategoria', required=False, queryset=(Category.objects.all()))

    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            return title

    class Meta:
        model = Article
        widgets = {
            'cover': FileInput(attrs={'class': 'hidden', 'id': 'change_cover'}),
            'title': TextInput(attrs={'class': 'width100 form-control '}),
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

    def clean_cover(self):
        cover = self.cleaned_data['cover']
        if cover is None:
            raise ValidationError("Nie dodano obrazu dla artykułu.")
        else:
            return cover


class SearchArticleForm(Form):
    def __init__(self, *args, **kwargs):
        super(SearchArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['category'].choices = [(c.pk, c.name) for c in Category.objects.all()]
        self.fields['search'].label = False

    category = MultipleChoiceField(label='kategoria', required=False, choices=[])
    title = CharField(label='tytuł', required=False)
    author = ChoiceField(label='autor', required=False)
    subtitle = CharField(label='podtytuł', required=False)
    published = ChoiceField(label='opublikowany', required=False)
    is_published = DateField(label='data publikacji', required=False)
    created = DateField(label='data utworzenia', required=False)
    search = CharField(label='', widget=TextInput())


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        model = Component
        fields = ('image', 'header', 'kind')
        widgets = {
            'image': FileInput(attrs={'class': 'hidden', 'id': 'add_image'}),
            'header': TextInput(attrs={'class': 'width100 form-control'})
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
            'header': TextInput(attrs={'class': 'width100 form-control'}),
            'text': TextInput(attrs={'class':'form-control'}),
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
            'header': TextInput(attrs={'class': 'width100 form-control'}),
            'quote': Textarea(attrs={'id': 'id_quote', 'class': 'width100 form-control', "rows":"1"}),
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
            'header': TextInput(attrs={'class': 'width100 form-control'}),
            'url': TextInput(attrs={'id': 'id_url', 'class': 'width100'})
        }
        labels = {'header': 'tytuł video',
                  'url': 'adres URL'}


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['cover'].required = False

    class Meta:
        model = Category
        fields = ['name', 'cover']
        widgets = {
            'cover': FileInput(attrs={'class': 'hidden', 'id': 'add_image'}),
            'name': TextInput(attrs={'class': 'width100 form-control'})
        }
        labels = {
            'name': 'nazwa działu'
        }


class PasswordRemindForm(Form):
    def __init__(self, *args, **kwargs):
        super(PasswordRemindForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    email = EmailField(label='email', required=True)


    def clean_email(self):
        cleaned_data = super(PasswordRemindForm, self).clean()
        email = cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        else:
            self.add_error('email', 'Nie istnieje konto o takim emailu.')
