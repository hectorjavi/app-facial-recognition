# Generated by Django 4.1.3 on 2023-11-23 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('work_environment', '0001_initial'),
        ('ia_model', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iamodel',
            name='work_environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='work_environment_ia_model', to='work_environment.workenvironment', verbose_name='Entorno de Desarrollo'),
        ),
        migrations.AlterUniqueTogether(
            name='iamodel',
            unique_together={('name', 'work_environment')},
        ),
    ]