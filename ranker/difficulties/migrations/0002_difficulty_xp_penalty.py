# Generated by Django 5.0 on 2024-09-28 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("difficulties", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="difficulty",
            name="xp_penalty",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="The amount of XP deducted whena challenge of this difficulty is failed.",
                verbose_name="XP Penalty",
            ),
            preserve_default=False,
        ),
    ]
