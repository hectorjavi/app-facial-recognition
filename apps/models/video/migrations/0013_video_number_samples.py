# Generated by Django 4.1.3 on 2023-10-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0012_alter_video_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="number_samples",
            field=models.PositiveSmallIntegerField(
                default=500, verbose_name="Número de muestras"
            ),
        ),
    ]
