# Generated by Django 4.0.4 on 2022-07-18 02:53

import club.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0018_remove_homeworksubmitmodel_homework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkfilesmodel',
            name='file',
            field=models.FileField(blank=True, upload_to=club.models.user_directory_path),
        ),
    ]