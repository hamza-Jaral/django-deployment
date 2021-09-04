from django import forms
from django.db.models import fields
from users.models import UserProfileInfo
from django.contrib.auth.models import User

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta(): 
        model = User
        fields = ('username', 'email', 'password')