from django.shortcuts import render
import json
import requests

# Set the API endpoint and headers
url = "https://Air-Quality-API.proxy-production.allthingsdev.co/v1/air-quality"
headers = {
    "x-apihub-key": "89PQuDoyMSCa8TLcFLZQ-wKZJgjgmPiIRo4whvngEDD5YMlGQg",
    "x-apihub-host": "Air-Quality-API.allthingsdev.co",
    "x-apihub-endpoint": "4ca197a3-ec74-4373-b962-9d39189c81bd"
}

# Predefined city coordinates
CITIES = {
    "yangon": {"latitude": 16.8409, "longitude": 96.1735},
    "bangkok": {"latitude": 13.7563, "longitude": 100.5018},
    "singapore": {"latitude": 1.3521, "longitude": 103.8198},
    "new york": {"latitude": 40.7128, "longitude": -74.0060},
    "los angeles": {"latitude": 34.0522, "longitude": -118.2437},
    "chicago": {"latitude": 41.8781, "longitude": -87.6298},
    "toronto": {"latitude": 43.651070, "longitude": -79.347015},
    "vancouver": {"latitude": 49.2827, "longitude": -123.1207},
    "london": {"latitude": 51.5074, "longitude": -0.1278},
    "paris": {"latitude": 48.8566, "longitude": 2.3522},
    "berlin": {"latitude": 52.52, "longitude": 13.405},
    "madrid": {"latitude": 40.4168, "longitude": -3.7038},
    "rome": {"latitude": 41.9028, "longitude": 12.4964},
    "amsterdam": {"latitude": 52.3676, "longitude": 4.9041},
    "oslo": {"latitude": 59.9139, "longitude": 10.7522},
    "copenhagen": {"latitude": 55.6761, "longitude": 12.5683},
    "stockholm": {"latitude": 59.3293, "longitude": 18.0686},
    "sydney": {"latitude": -33.8688, "longitude": 151.2093},
    "melbourne": {"latitude": -37.8136, "longitude": 144.9631},
    "beijing": {"latitude": 39.9042, "longitude": 116.4074},
    "shanghai": {"latitude": 31.2304, "longitude": 121.4737},
    "tokyo": {"latitude": 35.6762, "longitude": 139.6503},
    "seoul": {"latitude": 37.5665, "longitude": 126.9780},
    "hong kong": {"latitude": 22.3193, "longitude": 114.1694},
    "manila": {"latitude": 14.5995, "longitude": 120.9842},
    "delhi": {"latitude": 28.6139, "longitude": 77.2090},
    "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "karachi": {"latitude": 24.8607, "longitude": 67.0011},
    "jakarta": {"latitude": -6.2088, "longitude": 106.8456},
    "ho chi minh city": {"latitude": 10.8231, "longitude": 106.6297},
    "kuala lumpur": {"latitude": 3.1390, "longitude": 101.6869},
    "bangalore": {"latitude": 12.9716, "longitude": 77.5946},
    "chennai": {"latitude": 13.0827, "longitude": 80.2707},
    "lima": {"latitude": -12.0464, "longitude": -77.0428},
    "buenos aires": {"latitude": -34.6037, "longitude": -58.3816},
    "santiago": {"latitude": -33.4489, "longitude": -70.6693},
    "rio de janeiro": {"latitude": -22.9068, "longitude": -43.1729},
    "saopaulo": {"latitude": -23.5505, "longitude": -46.6333},
    "cape town": {"latitude": -33.9249, "longitude": 18.4241},
    "johannesburg": {"latitude": -26.2041, "longitude": 28.0473},
    "nairobi": {"latitude": -1.2867, "longitude": 36.8219},
    "lagos": {"latitude": 6.5244, "longitude": 3.3792},
    "abuja": {"latitude": 9.0579, "longitude": 7.4951},
    "casablanca": {"latitude": 33.5731, "longitude": -7.5898},
    "addis ababa": {"latitude": 9.145, "longitude": 40.4897},
    "doha": {"latitude": 25.276987, "longitude": 51.520008},
    "riyadh": {"latitude": 24.7136, "longitude": 46.6753},
    "cairo": {"latitude": 30.0444, "longitude": 31.2357},
    "madrid": {"latitude": 40.4168, "longitude": -3.7038},
    "moscow": {"latitude": 55.7558, "longitude": 37.6173},
    "vienna": {"latitude": 48.2082, "longitude": 16.3738},
    "zurich": {"latitude": 47.3769, "longitude": 8.5417},
    "milan": {"latitude": 45.4642, "longitude": 9.1900},
    "dublin": {"latitude": 53.3498, "longitude": -6.2603},
    "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "prague": {"latitude": 50.0755, "longitude": 14.4378},
    "athens": {"latitude": 37.9838, "longitude": 23.7275},
    "baku": {"latitude": 40.4093, "longitude": 49.8671},
    "astana": {"latitude": 51.1694, "longitude": 71.4491},
    "ho chi minh": {"latitude": 10.8231, "longitude": 106.6297},
    "helsinki": {"latitude": 60.1699, "longitude": 24.9384},
    "chile": {"latitude": -33.4489, "longitude": -70.6693},
    "kigali": {"latitude": -1.9706, "longitude": 30.1044},
    "bucarest": {"latitude": 44.4268, "longitude": 26.1025},
    "vienna": {"latitude": 48.2082, "longitude": 16.3738},
    "stockholm": {"latitude": 59.3293, "longitude": 18.0686},
    "geneva": {"latitude": 46.2044, "longitude": 6.1432},
    "berlin": {"latitude": 52.52, "longitude": 13.405},
    "amsterdam": {"latitude": 52.3676, "longitude": 4.9041},
    "rotterdam": {"latitude": 51.9225, "longitude": 4.4792},
    "liverpool": {"latitude": 53.4084, "longitude": -2.9916},
    "hamburg": {"latitude": 53.5511, "longitude": 9.9937},
    "brussels": {"latitude": 50.8503, "longitude": 4.3517},
    "monaco": {"latitude": 43.7333, "longitude": 7.4167},
    "luxembourg": {"latitude": 49.6117, "longitude": 6.13}
}

airquality_string = ""
# Create your views here.
def home(request):
    return render(request, 'home.html') 

def search_city(request):
    city = request.POST['city_name'] 
    if city.lower() not in CITIES:
        return render(request, 'result.html', {'error': "City not found."})

    # Fetch coordinates
    coords = CITIES[city.lower()]

    # Set the parameters for the API request
    params = {
        "latitude": coords["latitude"],
        "longitude":coords["longitude"],
        "hourly": "pm10",
        "current": "european_aqi",
        "domains": "auto",
        "timeformat": "iso8601",
        "timezone": "auto",
        "past_days": 1,
        "past_hours": 1,
        "forecast_days": 1,
        "forecast_hours": 1,
        "start_date": "",
        "end_date": "",
        "start_hour": "",
        "end_hour": "",
        "cell_selection": "nearest"
    }
    api_request = requests.get(url, headers=headers, params=params)
    
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error..."

    # Extract relevant data from the JSON response
    current_aqi = api['current']['european_aqi']
    

    # Determine air quality based on the European AQI
    if current_aqi <= 50:
        airquality_string = "Air Quality: Good"
        bg_class = "bg-good"
    elif current_aqi <= 100:
        airquality_string = "Air Quality: Moderate"
        bg_class = "bg-moderate"
    elif current_aqi <= 150:
        airquality_string = "Air Quality: Unhealthy for Sensitive Groups"
        bg_class = "bg-sensitive"
    elif current_aqi <= 200:
        airquality_string = "Air Quality: Unhealthy"
        bg_class = "bg-unhealthy"
    elif current_aqi <= 300:
        airquality_string = "Air Quality: Very Unhealthy"
        bg_class = "bg-very-unhealthy"
    else:
        airquality_string = "Air Quality: Hazardous"
        bg_class = "bg-hazardous"


     # 🔹 Return air quality data to the template
    return render(request, 'result.html', {
        'city': city.capitalize(),
        'aqi': current_aqi,
        'status': airquality_string,  # Make sure to pass it here
        "bg_class": bg_class
    })
 

def city_air_quality(request, city):    
    if city.lower() not in CITIES:
        return render(request, 'result.html', {'error': "City not found."})

    # Fetch coordinates
    coords = CITIES[city.lower()]

    # Set the parameters for the API request
    params = {
        "latitude": coords["latitude"],
        "longitude":coords["longitude"],
        "hourly": "pm10",
        "current": "european_aqi",
        "domains": "auto",
        "timeformat": "iso8601",
        "timezone": "auto",
        "past_days": 1,
        "past_hours": 1,
        "forecast_days": 1,
        "forecast_hours": 1,
        "start_date": "",
        "end_date": "",
        "start_hour": "",
        "end_hour": "",
        "cell_selection": "nearest"
    }
    api_request = requests.get(url, headers=headers, params=params)
    
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error..."

    # Extract relevant data from the JSON response
    current_aqi = api['current']['european_aqi']
    

    # Determine air quality based on the European AQI
    if current_aqi <= 50:
        airquality_string = "Air Quality: Good"
        bg_class = "bg-good"
    elif current_aqi <= 100:
        airquality_string = "Air Quality: Moderate"
        bg_class = "bg-moderate"
    elif current_aqi <= 150:
        airquality_string = "Air Quality: Unhealthy for Sensitive Groups"
        bg_class = "bg-sensitive"
    elif current_aqi <= 200:
        airquality_string = "Air Quality: Unhealthy"
        bg_class = "bg-unhealthy"
    elif current_aqi <= 300:
        airquality_string = "Air Quality: Very Unhealthy"
        bg_class = "bg-very-unhealthy"
    else:
        airquality_string = "Air Quality: Hazardous"
        bg_class = "bg-hazardous"


     # 🔹 Return air quality data to the template
    return render(request, 'result.html', {
        'city': city.capitalize(),
        'aqi': current_aqi,
        'status': airquality_string,  # Make sure to pass it here
        "bg_class": bg_class
    })

def about(request):
    return render(request, 'about.html',{})
