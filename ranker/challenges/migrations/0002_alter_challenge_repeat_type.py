# Generated by Django 5.0 on 2024-10-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="challenge",
            name="repeat_type",
            field=models.CharField(
                choices=[
                    ("once", "One time Only"),
                    ("daily", "Daily"),
                    ("weekly", "Weekly"),
                    ("monthly", "Monthly"),
                ],
                default="once",
                help_text="How often the challenge repeats.",
                max_length=10,
                verbose_name="Repeat type",
            ),
        ),
    ]
