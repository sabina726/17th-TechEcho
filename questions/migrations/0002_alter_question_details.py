# Generated by Django 5.1 on 2024-09-05 05:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="details",
            field=models.TextField(
                validators=[
                    django.core.validators.MinLengthValidator(
                        20, "問題描述至少要二十個字"
                    )
                ]
            ),
        ),
    ]
