# Generated by Django 4.0.4 on 2022-06-20 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0009_alter_commentsmodel_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessagesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full name')),
                ('email', models.EmailField(max_length=150, verbose_name='Email')),
                ('message', models.TextField(max_length=1500, verbose_name='Your message')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('replied', models.BooleanField(default=False)),
            ],
        ),
    ]
