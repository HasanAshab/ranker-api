# Generated by Django 5.0 on 2024-05-01 05:59

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="status",
            name="dark_color",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                help_text="The display color for dark theme.",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="Dark Color",
            ),
        ),
        migrations.AddField(
            model_name="status",
            name="light_color",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                help_text="The display color for ligth theme.",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="Ligth Color",
            ),
        ),
    ]
