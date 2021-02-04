from django.shortcuts import render
import requests
from .models import Campground
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

        # for i in spots:
        #     if request.post:
        #         camp_data = Campsite(
        #             name = []
        #         )


    return render(request, 'landing.html', {'all_campsites': all_campsites})

def pocketbook(request):
    campgrounds = Campground.objects.all()
    return render(request, 'campgrounds/pocketbook.html', {'campgrounds': campground})


   