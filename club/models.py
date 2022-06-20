from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class ProfileModel(models.Model):
    LANGUAGES = (
        ('EN', 'English'),
        ('RU', 'Russian'),
        ('GER', 'German')
    )
    LANG_LEVELS = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1')
    )
    AGE = (
        ('7-11', '7-11'),
        ('12-15', '12-15'),
        ('16-18', '16-18'),
        ('>18', '>18')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField('Your full name', max_length=150)
    telegram = models.CharField('Nickname on Telegram (if you have it)', max_length=100, blank=True)
    language = models.CharField('Your target language', max_length=3, choices=LANGUAGES)
    language_level = models.CharField('Level of your target language', max_length=2, choices=LANG_LEVELS)
    age = models.CharField('Your age', max_length=5, choices=AGE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class CommentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField('Your comment', max_length=5000)
    create_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.comment


class ContactMessagesModel(models.Model):
    full_name = models.CharField('Full name', max_length=100)
    email = models.EmailField('Email', max_length=150)
    message = models.TextField('Your message', max_length=1500)
    create_date = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return self.message
