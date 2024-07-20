import requests

def get_weather(lat, long):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid=c3cb361a5537e857517e24dd408258cb"
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()
        # Extract the weather information you need from the JSON response
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        #print(temperature, description)
        if description == 'clear sky':
            description=1
        elif description in ['thunderstorm','heavy thunderstorm','heavy rain','heavy snow']:
            description=2
        elif description == 'sleet':
            description=3
        elif description in ['few clouds','scattered clouds','broken clouds','overcast clouds']:
            description=4
        elif description in ['mist','fog','haze']:
            description=5
        else:
            description=6