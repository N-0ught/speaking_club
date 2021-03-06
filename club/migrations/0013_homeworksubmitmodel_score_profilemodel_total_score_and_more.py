# Generated by Django 4.0.4 on 2022-07-17 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0012_homeworksubmitmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworksubmitmodel',
            name='score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='total_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='homeworksubmitmodel',
            name='questions',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Ask our teachers anything'),
        ),
        migrations.AlterField(
            model_name='homeworksubmitmodel',
            name='status',
            field=models.CharField(choices=[('ND', 'Not done'), ('S', 'Submitted'), ('A', 'Accepted'), ('D', 'Denied')], default='ND', max_length=2, verbose_name='Day status'),
        ),
    ]
