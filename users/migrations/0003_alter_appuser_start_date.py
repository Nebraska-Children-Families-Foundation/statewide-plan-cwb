# Generated by Django 4.2.9 on 2024-02-05 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_appuser_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 16, 32, 26, 44249, tzinfo=datetime.timezone.utc), verbose_name='start date'),
        ),
    ]
