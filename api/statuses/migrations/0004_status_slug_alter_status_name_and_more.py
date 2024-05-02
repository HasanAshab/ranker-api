# Generated by Django 5.0 on 2024-05-01 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0003_alter_status_name_alter_status_required_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="status",
            name="slug",
            field=models.SlugField(
                default="jdjdj",
                help_text="The slugyfied version of the status name.",
                max_length=30,
                unique=True,
                verbose_name="Slug",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(
                help_text="The display name of the status",
                max_length=60,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="required_level",
            field=models.IntegerField(
                help_text="Minimum level requirement to achieve the level",
                verbose_name="Required Level",
            ),
        ),
    ]
