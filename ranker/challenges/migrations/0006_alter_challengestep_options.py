# Generated by Django 5.0 on 2024-07-07 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0005_remove_challenge_parent_challengestep"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="challengestep",
            options={"ordering": ("order", "id")},
        ),
    ]