# Generated by Django 5.0 on 2024-05-07 13:49

import api.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_usermodel_rank_alter_usermodel_total_xp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermodel",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")],
                default="M",
                help_text="Gender of the user",
                max_length=1,
                verbose_name="Gender",
            ),
        ),
        migrations.AlterField(
            model_name="usermodel",
            name="rank",
            field=models.PositiveBigIntegerField(
                default=api.users.models.get_default_rank,
                help_text="Global rank of the user",
                verbose_name="Rank",
            ),
        ),
    ]
