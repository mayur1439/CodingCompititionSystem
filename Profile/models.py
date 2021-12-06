from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile_det(models.Model):
	user_id = models.CharField(max_length=20,primary_key=True)
	user_name = models.CharField(max_length=50)
	email=models.CharField(max_length=50)
	dob = models.CharField(max_length=15)
	gender = models.CharField(max_length=10)
	Profession = models.CharField(max_length=15)
	University = models.CharField(max_length=100)
	contact=models.CharField(max_length=10)
	moto=models.CharField(max_length=100)
