# Generated by Django 5.0 on 2024-06-04 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("level_titles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leveltitle",
            options={"ordering": ("-required_level",)},
        ),
    ]