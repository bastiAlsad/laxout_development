# Generated by Django 5.0 on 2024-01-26 16:32

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(default='', max_length=200)),
                ('coupon_text', models.CharField(default='', max_length=400)),
                ('coupon_image_url', models.CharField(default='', max_length=200)),
                ('coupon_price', models.IntegerField(default=0)),
                ('coupon_offer', models.CharField(default='', max_length=100)),
                ('rabbat_code', models.CharField(default='', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DoneExercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_id', models.IntegerField(default=0)),
                ('laxout_user_id', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 1, 26, 17, 32, 50, 151974))),
            ],
        ),
        migrations.CreateModel(
            name='DoneWorkouts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_id', models.IntegerField(default=0)),
                ('laxout_user_id', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 1, 26, 17, 32, 50, 151974))),
            ],
        ),
        migrations.CreateModel(
            name='First',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='IndexesLaxoutUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('creation_date', models.IntegerField(default=1)),
                ('created_by', models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='IndexesPhysios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indexs', models.IntegerField(default=0)),
                ('logins', models.IntegerField(default=0)),
                ('tests', models.IntegerField(default=0)),
                ('for_month', models.IntegerField(default=1)),
                ('for_year', models.IntegerField(default=2024)),
                ('created_by', models.IntegerField(blank=True, default=None)),
                ('zero_two', models.IntegerField(default=0)),
                ('theree_five', models.IntegerField(default=0)),
                ('six_eight', models.IntegerField(default=0)),
                ('nine_ten', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LaxoutUserPains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_month', models.IntegerField(default=1)),
                ('created_by', models.IntegerField(blank=True, default=None)),
                ('zero_two', models.IntegerField(default=0)),
                ('theree_five', models.IntegerField(default=0)),
                ('six_eight', models.IntegerField(default=0)),
                ('nine_ten', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PhysioIndexCreationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_month', models.IntegerField(default=1)),
                ('for_year', models.IntegerField(default=2024)),
                ('created_by', models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Second',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SkippedExercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skipped_exercise_id', models.IntegerField(default=0)),
                ('laxout_user_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Laxout_Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution', models.CharField(default='', max_length=400)),
                ('name', models.CharField(default='', max_length=40)),
                ('dauer', models.IntegerField(default=30)),
                ('videoPath', models.CharField(default='', max_length=100)),
                ('looping', models.BooleanField(default=False)),
                ('added', models.BooleanField(default=False)),
                ('instruction', models.CharField(default='', max_length=200)),
                ('timer', models.BooleanField(default=False)),
                ('required', models.CharField(default='', max_length=50)),
                ('imagePath', models.CharField(default='', max_length=50)),
                ('appId', models.IntegerField(default=0)),
                ('onlineVideoPath', models.CharField(default='', max_length=220)),
                ('ignore', models.BooleanField(default=True)),
                ('first', models.ManyToManyField(to='laxout_app.first')),
                ('second', models.ManyToManyField(to='laxout_app.second')),
            ],
        ),
        migrations.CreateModel(
            name='LaxoutUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uid', models.CharField(default='', max_length=420)),
                ('laxout_user_name', models.CharField(default='', max_length=200)),
                ('laxout_credits', models.IntegerField(default=0)),
                ('note', models.CharField(default='', max_length=200)),
                ('creation_date', models.DateField(default=datetime.datetime(2024, 1, 26, 16, 32, 50, 155974, tzinfo=datetime.timezone.utc))),
                ('last_login', models.DateTimeField(default=datetime.datetime(2023, 11, 14, 0, 0))),
                ('last_login_2', models.DateTimeField(default=datetime.datetime(2023, 11, 14, 0, 0))),
                ('last_meet', models.DateField(default=datetime.datetime(2024, 1, 26, 17, 32, 50, 155975))),
                ('instruction', models.CharField(default='', max_length=200)),
                ('coupons', models.ManyToManyField(to='laxout_app.coupon')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exercises', models.ManyToManyField(to='laxout_app.laxout_exercise')),
                ('indexes', models.ManyToManyField(to='laxout_app.indexeslaxoutuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indexes', models.ManyToManyField(to='laxout_app.indexesphysios')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
