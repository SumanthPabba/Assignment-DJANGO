from django import forms
from .models import Profile
from django.forms import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def mobile_no(value):
  mobile = str(value)
  if len(mobile) != 10:
    raise forms.ValidationError("Mobile Number Should be 10 digit")


class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  phone_number = forms.CharField(max_length=10, validators=[mobile_no])
  address = forms.CharField(max_length=300)

  class Meta:
    model = User
    fields = ['username', 'email','password1', 'password2', 'phone_number', 'address']

class UserUpdateForm(forms.ModelForm):
  class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'address']

