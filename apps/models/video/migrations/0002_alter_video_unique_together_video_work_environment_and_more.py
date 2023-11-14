# Generated by Django 4.1.3 on 2023-10-07 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("work_environment", "0002_workenvironment_created_by"),
        ("video", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="video",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="video",
            name="work_environment",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="created_by_video",
                to="work_environment.workenvironment",
                verbose_name="Entorno de Desarrollo",
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="video",
            unique_together={("name", "work_environment")},
        ),
        migrations.RemoveField(
            model_name="video",
            name="created_by",
        ),
    ]