# Generated by Django 4.1.3 on 2023-10-07 23:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("work_environment", "0002_workenvironment_created_by"),
        ("ia_model", "0002_iamodel_work_environment"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="iamodel",
            unique_together={("name", "work_environment")},
        ),
    ]