# Generated by Django 5.0 on 2024-05-01 15:11

import django.contrib.auth.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "users",
            "0003_remove_usermodel_level_usermodel_total_points_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermodel",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="",
                help_text="Avatar (or profile pic) of the user",
                upload_to="uploads/avatars/",
                verbose_name="Avatar",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="usermodel",
            name="name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Name of the user",
                max_length=255,
                verbose_name="Name",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="usermodel",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                default="",
                help_text="Phone number of the user",
                max_length=128,
                region=None,
                verbose_name="Phone Number",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="usermodel",
            name="username",
            field=models.CharField(
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text="Required. 35 characters or fewer.Letters, digits and @/./+/-/_ only.",
                max_length=35,
                unique=True,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator()
                ],
                verbose_name="Username",
            ),
        ),
    ]
