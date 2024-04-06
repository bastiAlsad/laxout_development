from django.db import models
from django.contrib.auth.models import User
import random, string
from django.contrib.auth.models import AbstractUser,PermissionsMixin, User
from datetime import datetime
from django.utils import timezone
from uuid import uuid4

def random_string(length=70):
    allowed_characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(allowed_characters) for _ in range(length))
    return random_string

def generate_rabatt_code():
    allowed_characters = string.ascii_letters+string.digits
    random_string = ""
    for _ in range(10):
        random_string += random.choice(allowed_characters)

class DoneWorkouts(models.Model):
    workout_id = models.IntegerField(default = 0)
    laxout_user_id = models.IntegerField(default = 0)
    date = models.DateTimeField(default = datetime.now())


class DoneExercises(models.Model):
    exercise_id = models.IntegerField(default = 0)
    laxout_user_id = models.IntegerField(default = 0)
    date = models.DateTimeField(default = timezone.datetime.today())

class SkippedExercises(models.Model):
    skipped_exercise_id = models.IntegerField(default = 0)
    laxout_user_id = models.IntegerField(default = 0)

class IndexesLaxoutUser(models.Model):
    index = models.IntegerField(default=0)
    creation_date = models.IntegerField(default=datetime.now().month)
    created_by = models.IntegerField(default=None, blank=True)

class IndexesPhysios(models.Model):
    indexs = models.IntegerField(default=0)
    logins = models.IntegerField(default=0)
    tests = models.IntegerField(default=0)
    for_month = models.IntegerField(default=datetime.now().month)
    for_year = models.IntegerField(default=datetime.now().year)
    for_week = models.IntegerField(default = datetime.now().isocalendar()[1])
    created_by = models.IntegerField(default=None, blank=True)
    zero_two = models.IntegerField(default= 0)
    theree_five = models.IntegerField(default= 0)
    six_eight = models.IntegerField(default= 0)
    nine_ten = models.IntegerField(default= 0)

class LaxoutUserPains(models.Model):
    def __str__(self):
        return f"{self.created_by}'s Pains"
    for_month = models.IntegerField(default=datetime.now().month)
    created_by = models.IntegerField(default=None, blank=True)
    for_year = models.IntegerField(default=datetime.now().year)
    zero_two = models.IntegerField(default= 0)
    theree_five = models.IntegerField(default= 0)
    six_eight = models.IntegerField(default= 0)
    nine_ten = models.IntegerField(default= 0)
    for_week = models.IntegerField(default = datetime.now().isocalendar()[1])
    admin_id = models.IntegerField(default=0, blank=True)

class Coupon(models.Model):
    coupon_name = models.CharField(default="", max_length=200)
    coupon_text = models.CharField(default="", max_length=400)
    coupon_image_url = models.CharField(default="", max_length=200)
    coupon_price = models.IntegerField(default=0)
    coupon_offer = models.CharField(default="", max_length=100)
    rabbat_code = models.CharField(default="", max_length=250)


class First(models.Model):
    first = models.IntegerField(default = 0)

class Second(models.Model):
    second = models.IntegerField(default = 0)



class Laxout_Exercise(models.Model):
    execution = models.CharField(max_length=10000,default="")
    name = models.CharField(max_length=40,default="")
    dauer = models.IntegerField(default=30)
    videoPath = models.CharField(max_length=100,default="")
    looping = models.BooleanField(default=False)
    added = models.BooleanField(default=False)
    instruction = models.CharField(max_length=200, default="")
    timer = models.BooleanField(default=False)
    required = models.CharField(max_length=50, default="")
    imagePath = models.CharField(max_length=50, default="")
    appId = models.IntegerField(default=0)
    onlineVideoPath = models.CharField(default = "", max_length = 220)

class Laxout_Exercise_Order_For_User(models.Model):
    laxout_user_id = models.IntegerField(default = 0)
    laxout_exercise_id = models.IntegerField(default = 0)
    order = models.IntegerField(default = 0)


class LaxoutUser(models.Model):
    user_uid = models.CharField(max_length=420, default="")
    laxout_user_name = models.CharField(max_length=200, default="")
    laxout_credits = models.IntegerField(default=0)
    note = models.CharField(max_length=200, default="")
    creation_date = models.DateField(default= timezone.now())
    exercises = models.ManyToManyField(Laxout_Exercise)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    indexes = models.ManyToManyField(IndexesLaxoutUser)
    last_login = models.DateTimeField(default=timezone.datetime(2023, 11, 14))
    last_login_2 = models.DateTimeField(default = timezone.datetime(2023, 11, 14))
    coupons = models.ManyToManyField(Coupon)
    last_meet = models.DateField(default = timezone.datetime.today())
    instruction = models.CharField(default = "", max_length = 200)
    lax_tree_id = models.IntegerField(default = 0)
    water_drops_count = models.IntegerField(default = 0)
    instruction_in_int = models.IntegerField(default = 0)
    email_adress = models.CharField(default = "", max_length =40)
    admin_has_seen_chat = models.BooleanField(default = True)
    user_has_seen_chat = models.BooleanField(default = True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indexes = models.ManyToManyField(IndexesPhysios)

class PhysioIndexCreationLog(models.Model):
    for_month = models.IntegerField(default = datetime.now().month)
    for_year = models.IntegerField(default = datetime.now().year)
    created_by = models.IntegerField(default=None, blank=True)
    for_week = models.IntegerField(default = datetime.now().isocalendar()[1])


class LaxoutUserIndexCreationLog(models.Model):
    for_month = models.IntegerField(default = datetime.now().month)
    for_year = models.IntegerField(default = datetime.now().year)
    created_by = models.IntegerField(default=None, blank=True)
    for_week = models.IntegerField(default = datetime.now().isocalendar()[1])
    related_user_pain = models.IntegerField(default = 0)



class Uebungen_Models(models.Model):
    execution = models.CharField(max_length=10000,default="")
    name = models.CharField(max_length=40,default="")
    dauer = models.IntegerField(default=30)
    videoPath = models.CharField(max_length=100,default="")
    looping = models.BooleanField(default=False)
    added = models.BooleanField(default=False)
    instruction = models.CharField(max_length=200, default="")
    timer = models.BooleanField(default=False)
    required = models.CharField(max_length=50, default="")
    imagePath = models.CharField(max_length=50, default="")
    appId = models.IntegerField(default=0)
    onlineVideoPath = models.CharField(default = "", max_length = 220)
    first = models.ManyToManyField(First)
    second = models.ManyToManyField(Second)

class LaxTree(models.Model):
    condition = models.IntegerField(default = 0)

class SuccessControll(models.Model):
    better = models.BooleanField(default = False)
    created_by = models.IntegerField(default = 0)

class AiExercise(models.Model):
    exercise_id = models.IntegerField(default = 0)

class AiTrainingData(models.Model):
    illness = models.CharField(default = "", max_length = 200)
    related_exercises = models.ManyToManyField(AiExercise)
    created_by = models.IntegerField(default = 0) # Physio Id
    created_for = models.IntegerField(default =0) # LaxoutUserId 

class ChatDataModel(models.Model):
    is_sender = models.BooleanField(default = False)
    message = models.CharField(max_length = 2003000000, default = "")
    created_by = models.IntegerField(default = 0)
    admin_id = models.IntegerField(default = 0)

class BillingCount(models.Model):
    billing_count = models.IntegerField(default=1)