# Generated by Django 5.0 on 2024-05-01 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "difficulties",
            "0003_remove_difficulty_color_difficulty_dark_color_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="difficulty",
            options={"ordering": ("xp_value",)},
        ),
        migrations.RemoveField(
            model_name="difficulty",
            name="points",
        ),
        migrations.AddField(
            model_name="difficulty",
            name="xp_value",
            field=models.PositiveIntegerField(
                default=20,
                help_text="Number of xp value associated with this difficulty level.",
                verbose_name="XP Value",
            ),
            preserve_default=False,
        ),
    ]