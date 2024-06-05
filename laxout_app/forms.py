from django import forms
from .models import LaxoutUser, Uebungen_Models
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "email_adress"]


 # not  fields = ["laxout_user_name, note"] !


class User(forms.ModelForm):
    model = User
    fields = ["username", "password"]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Uebungen_Models
        fields = ["execution", "name", "dauer", "videoPath", "looping", "timer", "required", "imagePath", "onlineVideoPath", ]

class TrainingDataForm(forms.Form):
    illness = forms.CharField(max_length=100, required=True)
    
    