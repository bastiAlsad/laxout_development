# Generated by Django 5.0.4 on 2024-04-24 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0015_alter_doneexercises_date_alter_doneworkouts_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laxoutuser',
            name='was_created_through_app',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='doneexercises',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 24, 15, 32, 14, 639721)),
        ),
        migrations.AlterField(
            model_name='doneworkouts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 24, 15, 32, 14, 638721)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2024, 4, 24, 13, 32, 14, 641722, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='last_meet',
            field=models.DateField(default=datetime.datetime(2024, 4, 24, 15, 32, 14, 641722)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='user_has_seen_chat',
            field=models.BooleanField(default=False),
        ),
    ]
