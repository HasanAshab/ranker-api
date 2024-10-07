# Generated by Django 5.0 on 2024-10-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_usermodel_level_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermodel",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                help_text="Gender of the user",
                max_length=6,
                verbose_name="Gender",
            ),
        ),
    ]
