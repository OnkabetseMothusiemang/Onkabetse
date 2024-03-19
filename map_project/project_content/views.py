from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from .models import *
import googlemaps
from django.conf import settings
from .forms import *
from datetime import datetime

class HomeView(ListView):
    template_name = "project_content/home.html"
    context_object_name = 'mydata'
    model = Locations
    success_url = "/"

class MapView(View): 
    template_name = "project_content/map.html"

    def get(self,request): 
        key = 'AIzaSyANyEAM-XJv4DlL4h1yJlo0VwHBMMqDvHc'
        eligable_locations = Locations.objects.filter(place_id__isnull=False)
        locations = []

        for a in eligable_locations: 
            data = {
                'lat': float(a.lat), 
                'lng': float(a.lng), 
                'name': a.name
            }

            locations.append(data)


        context = {
            "key":key, 
            "locations": locations
        }

        return render(request, self.template_name, context)

class DistanceView(View):
    template_name = "project_content/distance.html"

    def get(self, request): 
        form = DistanceForm
        distances = Distances.objects.all()
        context = {
            'form':form,
            'distances':distances
        }

        return render(request, self.template_name, context)

    def post(self, request): 
        form = DistanceForm(request.POST)
        if form.is_valid(): 
            from_location = form.cleaned_data['from_location']
            from_location_info = Locations.objects.get(name=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Locations.objects.get(name=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                    from_adress_string,
                    to_adress_string,
                    mode = mode,
                    departure_time = now
            )


            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]: 
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else: 
                duration_in_traffic_minutes = None

            
            obj = Distances(
                from_location = Locations.objects.get(name=from_location),
                to_location = Locations.objects.get(name=to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
                duration_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        else: 
            print(form.errors)
        
        return redirect('my_distance_view')


class GeocodingView(View):
    template_name = "project_content/geocoding.html"

    def get(self,request,pk): 
        location = Locations.objects.get(pk=pk)

        if location.lng and location.lat and location.place_id != None: 
            lat = location.lat
            lng = location.lng
            place_id = location.place_id
            label = "from my database"

        elif location.adress and location.country and location.zipcode and location.city != None: 
            adress_string = str(location.adress)+", "+str(location.zipcode)+", "+str(location.city)+", "+str(location.country)

            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            result = gmaps.geocode(adress_string)[0]
            
            lat = result.get('geometry', {}).get('location', {}).get('lat', None)
            lng = result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id = result.get('place_id', {})
            label = "from my api call"

            location.lat = lat
            location.lng = lng
            location.place_id = place_id
            location.save()

        else: 
            result = ""
            lat = ""
            lng = ""
            place_id = ""
            label = "no call made"

        context = {
            'location':location,
            'lat':lat, 
            'lng':lng, 
            'place_id':place_id, 
            'label': label
        }
        
        return render(request, self.template_name, context)


from django.shortcuts import render
from .models import Locations  # Import your Location model

def my_view(request):
    locations = Locations.objects.all()  # Assuming Location is a model with location data
    return render(request, 'map.html', {'locations': locations})

from django.shortcuts import render
import json

def map_view(request):
    locations = [
        {'lat': 51.505, 'lng': -0.09, 'name': 'Location 1'},
        {'lat': 52.0, 'lng': -1.0, 'name': 'Location 2'},
        {'lat': -25.4525, 'lng': 28.1088, 'name': 'New Location'},  # Add the new location here
    ]
    locations_json = json.dumps(locations)
    return render(request, 'map.html', {'locations': locations_json})


#Tvehicle tracking
# views.py
from django.shortcuts import render
from .models import Order, Location

def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    locations = Location.objects.filter(order=order).order_by('-timestamp')
    return render(request, 'order_detail.html', {'order': order, 'locations': locations})

#saving location
# views.py

from django.shortcuts import render
from .models import Location
from django.http import JsonResponse

def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Save the location to the database
        Location.objects.create(latitude=latitude, longitude=longitude)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
# views.py

from django.shortcuts import render

def delivery_route(request):
    
    start_latitude = -25.5502
    start_longitude = 28.0897
    user_latitude = 0  
    user_longitude = 0  
    google_maps_api_key = 'AIzaSyCZJCJVzkTMgNFmi6SXU3IVcRiUt6luZIk'  
    
    return render(request, 'delivery_route.html')


