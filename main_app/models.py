from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
from django.db import models

# Create your models here.

class Campground(models.Model):
    name = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=20, default='')
    zipcode = models.CharField(max_length=15, default='')
    phone = models.CharField(max_length=15, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'campground_id': self.id})

class Trip(models.Model):
    startdate = models.DateField('Start Date')
    enddate = models.DateField('End Date')
    reservation_link = models.CharField(max_length=500, default='')

    campground = models.ForeignKey(Campground, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'campground_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    campground = models.ForeignKey(Campground, on_delete=models.CASCADE)
    

    def get_absolute_url(self):
        return f"Photo for campground_id: {self.campground_id} @{self.url}"


   

