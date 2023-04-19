from django.db import models
from Users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Cars(models.Model):

    dealerName = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dealername')
    CarName = models.CharField(max_length=30)
    ModelName = models.CharField(max_length=30)
    CarNumber = models.CharField(max_length=30)
    Features = models.TextField()
    IsAvailable = models.CharField(max_length=3)
    CarImage = models.ImageField(
        default='navimg.jpeg', upload_to='car_pics')
    fuelConsumption = models.CharField(max_length=10) 
    carInsurance = models.CharField(max_length=3)
    CostPerDay = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.CarNumber}"


class otherDetails(models.Model):

    username = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='carbookperson')
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=300)
    from_date = models.DateField()
    to_date = models.DateField()

# class History(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     car_name = models.ForeignKey(Cars, on_delete=models.CASCADE)
#     car_dealer_name = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=10)
#     address = models.CharField(max_length=300)
#     from_date = models.DateField()
#     to_date = models.DateField()
#     CostPerDay = models.CharField(max_length=10)
#     days = models.CharField(max_length=3)
#     Fare = models.IntegerField()