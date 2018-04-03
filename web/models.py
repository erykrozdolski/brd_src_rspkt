from django.utils import timezone
from django.db import models
from django.utils import timezone
from datetime import timedelta
from sorl.thumbnail import ImageField
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField



class User(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').null = False
    AbstractUser._meta.get_field('email').max_length = 80
    AbstractUser._meta.get_field('username').max_length = 80
    AbstractUser._meta.get_field('username')._unique = True

    AbstractUser._meta.get_field('last_name').blank = True
    AbstractUser._meta.get_field('last_name').max_length = 80
    AbstractUser._meta.get_field('first_name').blank = True
    AbstractUser._meta.get_field('first_name').max_length = 80
    AbstractUser._meta.get_field('is_active').default = True
    blocked_reason = models.TextField(default='',  blank=True, null=True)
    bio = models.TextField(default='', blank=True, null=True)
    avatar = ImageField(upload_to='web/media/avatars', null=True, blank=True)

    def block(self):
        self.is_active = False
        self.save()

    def unblock(self):
        self.is_active = True
        self.save()





class Article(models.Model):
    title = models.CharField(max_length=100, default='', blank=False, null=False, verbose_name='tytuł')
    subtitle = models.CharField(max_length=150, default='', blank=False, null=False, verbose_name='podtytuł')
    author = models.ForeignKey('User', null=True, blank=True, verbose_name='autor')
    created = models.DateTimeField(auto_now_add=True, verbose_name='utworzony')
    published = models.DateTimeField(null=True, blank=True, verbose_name='opublikowany')
    is_published = models.BooleanField(default=False, verbose_name="czy opublikowany")
    status = models.CharField(max_length=100, default="created", verbose_name='status')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='tagi')
    category = models.ForeignKey('Category', null=True, blank=True, verbose_name='dział')
    cover = ImageField(upload_to='web/media/covers', default="web/static/images/thumbnail.jpg", null=False, blank=False, verbose_name='okładka')
    components = models.ManyToManyField('Component')

    @classmethod
    def get_n_newest(cls, n=10):
        return cls.objects.filter(is_published=True).order_by('published')[0:n]

    @classmethod
    def get_main(cls):
        if cls.objects.filter(status='main_article').exists():
            return cls.objects.filter(status='main_article')
        else:
            if cls.objects.all():
                return cls.objects.all()[0]
            else:
                return None


    @classmethod
    def get_most_popular(cls):
        return cls.objects.filter(is_published=True)[:10]

    def publish(self):
        self.published = timezone.now()
        self.is_published = True
        self.status = 'published'
        self.save()
        return self.is_published

    def unpublish(self):
        self.published = None
        self.is_published = False
        self.status = 'unpublished'
        self.save()
        return self.is_published

    def when_was_published(self):
        today = timezone.now()
        if self.is_published:
            total_hours = (today - self.published).total_seconds() // 3600
            if total_hours < 24:
                return '{} godzin temu'.format(total_hours)
            elif 720 > total_hours > 24:
                return '{} dni temu'.format(int(total_hours / 24))
            elif total_hours > 720:
                return '{} miesięcy temu'.format(int(total_hours / 720))
        else:
            return False




component_kinds = (
    ('image', 'obraz'),
    ('quote', 'cytat'),
    ('text', 'kolumna'),
    ('url', 'film YT'),
)

class Component(models.Model):
    position = models.PositiveIntegerField(default=0, null=True, blank=True)
    header = models.CharField(max_length=50, blank=False, null=False, unique=False)
    kind = models.CharField(max_length=20, blank=False, null=False, choices=component_kinds)
    image = ImageField(upload_to='web/media/images', null=True, blank=True)
    quote = models.CharField(max_length=100, null=True, blank=False)
    url = models.CharField(max_length=250, null=True, blank=False)
    text = HTMLField(max_length=50, blank=False, null=False, unique=False, default="")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    cover = ImageField(upload_to='web/media/covers', null=False, blank=False, verbose_name='okładka')

    def __str__(self):
        return self.name


class Email_message(models.Model):
    receiver = models.EmailField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey('User', blank=True, null=True)
