# Generated by Django 5.1 on 2024-09-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_remove_question_downvote_remove_question_upvote_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionuservotes',
            name='vote_value',
        ),
        migrations.AddField(
            model_name='questionuservotes',
            name='vote_status',
            field=models.CharField(default='neither', max_length=10),
        ),
    ]
