# Generated by Django 5.0 on 2024-06-04 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("level_titles", "0002_alter_leveltitle_options"),
        ("users", "0002_usermodel_level_titles"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usermodel",
            name="level_titles",
        ),
        migrations.AddField(
            model_name="usermodel",
            name="level_title",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="level_titles.leveltitle",
            ),
            preserve_default=False,
        ),
    ]
