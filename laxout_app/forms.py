from django import forms
from .models import LaxoutUser, Uebungen_Models
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "note", "email_adress"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['note'].required = False
        self.fields['note'].label = 'Name der Neuen Diagnose'
 # not  fields = ["laxout_user_name, note"] !


class User(forms.ModelForm):
    model = User
    fields = ["username", "password"]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Uebungen_Models
        fields = ["execution", "name", "dauer", "videoPath", "looping", "timer", "required", "imagePath", "onlineVideoPath", ]