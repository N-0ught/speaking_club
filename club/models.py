from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
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
    total_score = models.FloatField(default=0)
    access = models.BooleanField(default=False)

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


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/Day_{1}/{2}'.format(instance.homework.user.username, instance.homework.day, filename)


class HomeworkSubmitModel(models.Model):
    STATUS = (
        ('ND', 'Not done'),
        ('S', 'Submitted'),
        ('A', 'Accepted'),
        ('D', 'Denied')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField('Course day', max_length=2)
    questions = models.TextField('Ask our teachers anything', max_length=2000, blank=True)
    score = models.FloatField(default=0)
    status = models.CharField('Day status', max_length=2, choices=STATUS, default='ND')

    def __str__(self):
        return f'{self.user}, {self.day}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_score = HomeworkSubmitModel.objects.filter(user=self.user).aggregate(Sum('score'))
        self.user.profilemodel.total_score = total_score['score__sum']
        self.user.profilemodel.save()

    def status_type_submit(user):
        data = HomeworkSubmitModel.objects.filter(user=user, status='S')
        return {int(day.day): day.status for day in data}

    def status_type_accepted(user):
        data = HomeworkSubmitModel.objects.filter(user=user, status='A')
        return {int(day.day): day.status for day in data}

    def status_type_denied(user):
        data = HomeworkSubmitModel.objects.filter(user=user, status='D')
        return {int(day.day): day.status for day in data}

    def days_completed(user):
        data = HomeworkSubmitModel.objects.filter(user=user, status='A')
        return len(data)


class HomeworkFilesModel(models.Model):
    homework = models.ForeignKey(HomeworkSubmitModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path, blank=True)


class ChatMessages(models.Model):
    page = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create_date']
