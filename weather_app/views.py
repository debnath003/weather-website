from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import datetime
import pytz  # Import pytz for timezone handling
import urllib.parse
from .models import SavedCity
from django.contrib import messages

API_KEY = 'b75279e94cc230e5fb92dbccb62c3053'  # Replace with your actual API key

def landing_page(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        time = request.POST.get('time')
        if not city and not time:
            return render(request, 'landing_page.html', {'error': 'Select a city and time!'})
        elif not city:
            return render(request, 'landing_page.html', {'error': 'Select a city!'})
        elif not time:
            return render(request, 'landing_page.html', {'error': 'Select a time!'})

        # Redirect to weather details page
        return redirect('weather_details', city=city, time=time)

    return render(request, 'landing_page.html')

def weather_details(request):
    city = request.GET.get('city')
    time_str = request.GET.get('time')

    if not city or not time_str:
        return render(request, 'landing_page.html', {'error': 'City and time are required!'})

    try:
        time = datetime.datetime.strptime(time_str, '%H:%M')
    except ValueError:
        return render(request, 'landing_page.html', {'error': 'Invalid time format!'})

    city = city.capitalize()
    encoded_city = urllib.parse.quote(city)

    # Fetch current weather data
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={API_KEY}&units=metric'
    try:
        current_weather_response = requests.get(current_weather_url)
        current_weather_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        current_weather_data = current_weather_response.json()
    except requests.exceptions.RequestException as e:
        return render(request, 'weather_details.html', {'error': f'Error fetching current weather data: {e}'})

    # Fetch 5-day forecast data
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={encoded_city}&appid={API_KEY}&units=metric'
    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Filter forecast data for the same time for the next 5 days
        forecast_list = forecast_data['list']
        forecast = []
        today = datetime.date.today()
        start_day = 1
        if time.hour in [18, 21]:
            start_day = 0

        for i in range(start_day, start_day + 5):
            target_date = today + datetime.timedelta(days=i)
            target_datetime = datetime.datetime(target_date.year, target_date.month, target_date.day, time.hour, time.minute, time.second)

            # Use UTC timezone for comparison
            utc_timezone = pytz.utc
            target_datetime = utc_timezone.localize(target_datetime)

            closest_forecast = min(forecast_list, key=lambda x: abs((datetime.datetime.fromtimestamp(x['dt'], tz=utc_timezone) - target_datetime).total_seconds()))

            # Add icon name to forecast item
            weather_description = closest_forecast['weather'][0]['description']
            closest_forecast['weather'][0]['icon'] = closest_forecast['weather'][0]['icon']
            forecast.append(closest_forecast)

    except requests.exceptions.RequestException as e:
        return render(request, 'weather_details.html', {'error': f'Error fetching forecast data: {e}'})

    context = {
        'city': city,
        'time': time.strftime('%H:%M'),
        'current_weather': {
            'temperature': current_weather_data['main']['temp'],
            'description': current_weather_data['weather'][0]['description'],
            'wind_speed': current_weather_data['wind']['speed'],
        },
        'forecast': forecast,
    }

    return render(request, 'weather_details.html', context)

def save_city(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        temperature = request.POST.get('temperature')
        time_str = request.POST.get('time')
        user_name = request.POST.get('userName')

        try:
            time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid time format!'})

        try:
            # Check if the city and temperature are already saved by any user
            if SavedCity.objects.filter(city=city, temperature=temperature, time=time_obj).exists():
                return JsonResponse({'status': 'warning', 'message': 'City saved earlier by user!'})

            # Save the city details
            saved_city = SavedCity(city=city, temperature=temperature, time=time_obj, user_name=user_name)
            saved_city.save()

            return JsonResponse({'status': 'success', 'message': 'City with the temperature saved!'})

            # Save the city details
            saved_city = SavedCity(city=city, temperature=temperature, time=time_obj, user_name=user_name)
            saved_city.save()

            return JsonResponse({'status': 'success', 'message': 'City with the temperature saved!'})

            # Save the city details
            saved_city = SavedCity(city=city, temperature=temperature, time=time_obj, user_name=user_name)
            saved_city.save()

            return JsonResponse({'status': 'success', 'message': 'City with the temperature saved!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

def saved_cities(request):
    saved_cities = SavedCity.objects.all()
    context = {'saved_cities': saved_cities}
    return render(request, 'saved_cities.html', context)

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_saved_cities_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city_ids = data.get('city_ids')
            csrf_token = data.get('csrfmiddlewaretoken')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format!'})

        if city_ids:
            try:
                SavedCity.objects.filter(id__in=city_ids).delete()
                return JsonResponse({'status': 'success', 'message': 'Selected city/cities deleted!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'warning', 'message': 'No city/cities deleted!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

def about(request):
    return render(request, 'about.html')
