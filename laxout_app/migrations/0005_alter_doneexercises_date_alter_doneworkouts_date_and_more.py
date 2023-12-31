# Generated by Django 5.0 on 2024-01-03 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0004_alter_doneexercises_date_alter_doneworkouts_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doneexercises',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 3, 18, 10, 39, 396108)),
        ),
        migrations.AlterField(
            model_name='doneworkouts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 3, 18, 10, 39, 396108)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 3, 17, 10, 39, 397108, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='last_meet',
            field=models.DateField(default=datetime.datetime(2024, 1, 3, 18, 10, 39, 398109)),
        ),
    ]
