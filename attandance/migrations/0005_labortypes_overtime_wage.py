# Generated by Django 4.2.5 on 2023-11-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attandance', '0004_attendancerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='labortypes',
            name='overtime_wage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
