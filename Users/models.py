from django.db import models
from django.contrib.auth.models import User
from django.core.validators import * 

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    email = models.EmailField(default='xyz@gmail.com')
    image = models.ImageField(default='user.jfif', upload_to='user_pics')
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=300)
    role = models.CharField(default='Customer', max_length=6)

    def __str__(self):
      return f'{self.user.username}'