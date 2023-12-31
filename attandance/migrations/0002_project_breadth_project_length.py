# Generated by Django 4.2.5 on 2023-11-01 12:07

import attandance.models
from django.db import migrations
import django_measurement.models
import measurement.measures.distance


class Migration(migrations.Migration):

    dependencies = [
        ('attandance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='Breadth',
            field=django_measurement.models.MeasurementField(default=attandance.models.default_length, measurement=measurement.measures.distance.Area),
        ),
        migrations.AddField(
            model_name='project',
            name='Length',
            field=django_measurement.models.MeasurementField(default=attandance.models.default_length, measurement=measurement.measures.distance.Area),
        ),
    ]
