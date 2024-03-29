# Generated by Django 5.0 on 2024-03-07 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0005_aiexercise_alter_doneexercises_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aitrainingdata',
            name='created_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='doneexercises',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 15, 30, 46, 740631)),
        ),
        migrations.AlterField(
            model_name='doneworkouts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 15, 30, 46, 739630)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 7, 14, 30, 46, 742630, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='last_meet',
            field=models.DateField(default=datetime.datetime(2024, 3, 7, 15, 30, 46, 742630)),
        ),
    ]
