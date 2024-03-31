# Generated by Django 5.0 on 2024-03-20 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0009_alter_doneexercises_date_alter_doneworkouts_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sender', models.BooleanField(default=False)),
                ('message', models.CharField(default='', max_length=2003000000)),
                ('created_by', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='doneexercises',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 15, 25, 48, 595480)),
        ),
        migrations.AlterField(
            model_name='doneworkouts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 15, 25, 48, 595480)),
        ),
        migrations.AlterField(
            model_name='indexesphysios',
            name='for_week',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 14, 25, 48, 597481, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='last_meet',
            field=models.DateField(default=datetime.datetime(2024, 3, 20, 15, 25, 48, 597482)),
        ),
        migrations.AlterField(
            model_name='laxoutuserindexcreationlog',
            name='for_week',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='laxoutuserpains',
            name='for_week',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='physioindexcreationlog',
            name='for_week',
            field=models.IntegerField(default=12),
        ),
    ]