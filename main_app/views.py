from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Campground, Photo, Trip
from .forms import TripForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import requests
import os

api_key = os.environ['API_KEY']
parameters = {"api_key":api_key} 

def landing(request):
    all_campsites = {}
    if 'stateCode' in request.GET:
        statecode = request.GET['stateCode']
        endpoint = "https://developer.nps.gov/api/v1/campgrounds?stateCode=%s" %statecode
        response = requests.get(endpoint, params=parameters)
        data_all = response.json()
        spots = data_all['data']
        all_campsites = spots
    return render(request, 'landing.html', {'all_campsites': all_campsites})

@login_required
def pocketbook(request):
    campgrounds = Campground.objects.filter(user=request.user)
    return render(request, 
    'campgrounds/pocketbook.html', 
    {'campgrounds': campgrounds}
    )

@login_required
def adventure_detail(request, campground_id):
    campground = Campground.objects.get(id=campground_id)
    trip_form = TripForm()
    return render(request, 'campgrounds/detail.html', {
        'campground': campground,
        'trip_form': trip_form
        })

@login_required
def add_trip(request, campground_id):
    form = TripForm(request.POST)
    if form.is_valid():
        new_trip = form.save(commit=False)
        new_trip.campground_id = campground_id
        new_trip.save()
        return redirect('detail', 
        campground_id=campground_id
        )

def add_photo(request):
    photos = Photo.objects.all()
    return render(request, 
    'campgrounds/photos.html', 
    {'photos': photos}
    )


class CampgroundCreate(LoginRequiredMixin, CreateView):
    model = Campground
    fields = '__all__'
    success_url = '/campgrounds/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CampgroundUpdate(LoginRequiredMixin, UpdateView):
    model = Campground
    fields = ['city', 'state', 'zipcode', 'phone', 'directions']

class CampgroundDelete(LoginRequiredMixin, DeleteView):
    model = Campground
    success_url = '/campgrounds/'

class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['startdate', 'enddate', 'reservation']



def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)




   