# Generated by Django 4.1.3 on 2023-10-08 21:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ia_model", "0008_alter_iamodel_labels_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iamodel",
            name="name",
            field=models.CharField(
                max_length=50,
                verbose_name="Nombre del modelo de inteligencia artificial",
            ),
        ),
    ]
