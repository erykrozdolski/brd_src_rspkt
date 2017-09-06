from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').null = False
    AbstractUser._meta.get_field('email').max_length = 80
    AbstractUser._meta.get_field('username').max_length = 80

    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('last_name').max_length = 80
    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('first_name').max_length = 80
    blocked_reason = models.TextField(default='')
    bio = models.TextField(default='')


class Article(models.Model):
    title = models.CharField(max_length=100, default='', blank=False, null=False, verbose_name='tytuł')
    subtitle = models.CharField(max_length=150, default='', blank=False, null=False, verbose_name='podtytuł')
    author = models.ForeignKey(User, null=True, blank=True, verbose_name='autor')
    created = models.DateTimeField(auto_now_add=True, verbose_name='utworzony')
    published = models.DateTimeField(null=True, blank=True, verbose_name='opublikowany')
    is_published = models.BooleanField(default=False, verbose_name="czy opublikowany")
    status = models.CharField(max_length=100, default="created", verbose_name='status')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='tagi')
    category = models.ForeignKey('Category', null=True, blank=True, verbose_name='dział')
    cover = ImageField(upload_to='web/media/covers', null=True, blank=True, verbose_name='okładka')
    components = models.ManyToManyField('Component')

    def publish(self):
        print('publikuję się')

        self.published = timezone.now()
        self.is_published = True
        self.save()
        print(self.is_published)
        return self.is_published


    def unpublish(self):
        print('unpublikuję się')
        self.published = None
        self.is_published = False
        self.save()
        print(self.is_published)
        return self.is_published


component_kinds = (
    ('image', 'obraz'),
    ('quote', 'cytat'),
    ('text', 'kolumna'),
    ('url', 'film YT'),
)

class Component(models.Model):
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    header = models.CharField(max_length=50, blank=False, null=False, unique=True)
    kind = models.CharField(max_length=20, blank=False, null=False, choices=component_kinds)
    image = ImageField(upload_to='web/media/images', null=True, blank=True)
    quote = models.CharField(max_length=100, null=True, blank=False)
    url = models.CharField(max_length=250, null=True, blank=False)
    text = models.TextField(null=True, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    cover = ImageField(upload_to='web/media/covers', null=False, blank=False, verbose_name='okładka')

    def __str__(self):
        return self.name
