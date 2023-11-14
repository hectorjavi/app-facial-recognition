# Generated by Django 4.1.3 on 2023-10-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0007_alter_video_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="label_name",
            field=models.CharField(
                blank=True,
                max_length=60,
                null=True,
                verbose_name="Nombre de la etiqueta",
            ),
        ),
    ]
