from django.shortcuts import render
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
   