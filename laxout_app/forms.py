from django import forms
from .models import LaxoutUser, Laxout_Exercise_Model
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "note"] # not  fields = ["laxout_user_name, note"] !


class User(forms.ModelForm):
    model = User
    fields = ["username", "password"]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Laxout_Exercise_Model
        fields = ["execution", "name", "dauer", "videoPath", "looping", "timer", "required", "imagePath", "onlineVideoPath", ]