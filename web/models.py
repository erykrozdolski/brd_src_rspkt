from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=100, default='', blank=False, null=False, verbose_name='tytuł')
    subtitle = models.CharField(max_length=150, default='', blank=False, null=False, verbose_name='podtytuł')
    author = models.ForeignKey(User, null=True, blank=True, verbose_name='autor')
    created = models.DateTimeField(auto_now_add=True, verbose_name='utworzony')
    published = models.DateTimeField(default=timezone.now, verbose_name='opublikowany')
    status = models.CharField(max_length=100, default="created", verbose_name='status')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='tagi')
    section = models.ForeignKey('Section', null=True, blank=True, verbose_name='dział')
    cover = models.ImageField(upload_to='web/media/covers', null=True, blank=False, verbose_name='okładka')
    components = models.ManyToManyField('Component')


class Component(models.Model):
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    header = models.CharField(max_length=50, blank=False, null=False)
    kind = models.CharField(max_length=20, blank=False, null=False)
    image = models.ImageField(upload_to='web/media/images', null=True, blank=False)
    quote = models.CharField(max_length=100, null=True, blank=False)
    url = models.CharField(max_length=250, null=True, blank=False)
    text = models.TextField(null=True, blank=False)


class Section(models.Model):
    name = models.CharField(max_length=100)
