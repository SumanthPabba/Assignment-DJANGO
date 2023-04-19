from django import forms
from django.forms import fields  
from Cars.models import Cars, otherDetails

def mobile_no(value):
  mobile = str(value)
  if len(mobile) != 10:
    raise forms.ValidationError("Mobile Number Should be 10 digit")

class CarDetailsForm(forms.ModelForm):

    class Meta:
        model = Cars
        fields = '__all__'


# class InputForm(forms.ModelForm):
    
#     # address = forms.CharField(max_length=300)
#     # phone_number = forms.CharField(max_length=10, validators=[mobile_no])
#     # from_date= forms.DateField()
#     # to_date= forms.DateField()

#     class Meta:

#         model = otherDetails
#         fields = ['address', 'phone_number', 'from_date', 'to_date']
