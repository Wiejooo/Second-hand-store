from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Clothes
from django import forms


class ClothesForm(ModelForm):

    class Meta:
        model = Clothes
        fields = ["name", "size", "price", "description", "gender", "img"]


class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['username', 'email', 'first_name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput())
    password = forms.CharField(max_length=63, widget=forms.PasswordInput())


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
