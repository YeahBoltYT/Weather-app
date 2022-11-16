from flask import Flask, render_template, request
import configparser
import requests
from datetime import datetime
app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'Fahrenheit':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = data["main"]["temp"]
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        maximum = data["main"]["temp_max"]
        minimum = data["main"]["temp_min"]
        letter = 'F'
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = data["main"]["temp"]
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        maximum = data["main"]["temp_max"]
        minimum = data["main"]["temp_min"]
        letter = 'C'
    icon = data["weather"][0]["icon"]
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    weather = data["weather"][0]["main"]
    location = data["name"]
    print(location)
    humidity = data["main"]["humidity"]
    print(humidity)
    # Sunrise (get and convert)
    sunrise = data["sys"]["sunrise"]
    sunrise = datetime.fromtimestamp(int(sunrise))
    print(sunrise)
    # current datetime for SA
    now = datetime.now().replace(microsecond=0)
    # current datetime for the user requested location
    now_utc = datetime.utcnow()
    timestamp_utc = datetime.timestamp(now_utc)
    tz_offset = int(data["timezone"])
    local_timestamp = timestamp_utc + tz_offset
    print(local_timestamp)
    local_datetime_obj = datetime.fromtimestamp(local_timestamp)

    return render_template('results.html',
                           location=location, temp=temp, iconurl=iconurl, feels_like=feels_like,
                           weather=weather, temp_units=temp_units, sunrise=sunrise, now=now, tz_offset=tz_offset,
                           now_utc=now_utc, humidity=humidity, minimum=minimum, maximum=maximum, letter=letter,
                           timestamp_utc=timestamp_utc, local_datetime_obj=local_datetime_obj, local_timestamp=local_timestamp)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run()

print(get_weather_results_imperial("zip_code", get_api_key()))
print(get_weather_results_metric("zip_code", get_api_key()))
