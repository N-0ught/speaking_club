# Generated by Django 4.0.4 on 2022-06-19 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0007_rename_message_commentsmodel_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsmodel',
            name='comment',
            field=models.TextField(max_length=5000, verbose_name='Your comment'),
        ),
    ]
