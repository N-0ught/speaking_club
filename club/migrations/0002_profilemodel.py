# Generated by Django 4.0.4 on 2022-05-17 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Your full name')),
                ('telegram', models.CharField(max_length=100, verbose_name='Nickname on Telegram (if you have it)')),
                ('language', models.CharField(choices=[('EN', 'English'), ('RU', 'Russian'), ('GER', 'German')], max_length=3, verbose_name='Your target language')),
                ('language_level', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1')], max_length=2, verbose_name='Level of your target language')),
                ('age', models.CharField(choices=[('7-11', '7-11'), ('12-15', '12-15'), ('16-18', '16-18'), ('>18', '>18')], max_length=5, verbose_name='Your age')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
