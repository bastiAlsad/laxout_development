# Generated by Django 5.0 on 2024-03-07 18:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0008_alter_doneexercises_date_alter_doneworkouts_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doneexercises',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 19, 28, 21, 421363)),
        ),
        migrations.AlterField(
            model_name='doneworkouts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 19, 28, 21, 421362)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 7, 18, 28, 21, 423363, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='last_meet',
            field=models.DateField(default=datetime.datetime(2024, 3, 7, 19, 28, 21, 423363)),
        ),
    ]