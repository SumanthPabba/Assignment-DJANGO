from django.contrib import admin
from .models import Cars, otherDetails
# Register your models here.

models = [Cars, otherDetails]
admin.site.register(models)