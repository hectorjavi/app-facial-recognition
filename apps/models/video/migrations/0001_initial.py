# Generated by Django 4.1.3 on 2023-11-23 03:44

import apps.models.video.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('work_environment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('video', models.FileField(upload_to=apps.models.video.models.generate_unique_filename, validators=[apps.models.video.models.validate_video_format], verbose_name='Video')),
                ('label', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Etiqueta')),
                ('label_name', models.CharField(max_length=60, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_]*$', 'Solo se permiten letras, números y guiones bajos.')], verbose_name='Nombre de la etiqueta')),
                ('number_samples', models.PositiveSmallIntegerField(default=500, verbose_name='Número de muestras')),
                ('work_environment', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='work_environment_video', to='work_environment.workenvironment', verbose_name='Entorno de Desarrollo')),
            ],
            options={
                'verbose_name': 'Registro "Video"',
                'verbose_name_plural': 'Tabla de registros "Video"',
                'db_table': 'video',
                'unique_together': {('label_name', 'work_environment')},
            },
        ),
    ]
