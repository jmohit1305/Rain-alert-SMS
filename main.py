import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

api_key = "OPEN_WEATHER_API"
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

parameters = {
    'lon': 77.2167,
    'lat': 28.6667,
    "appid": api_key,
    "exclude": "current,daily,minutely"
}

response = requests.get(url=OWM_ENDPOINT, params=parameters)

weather_data = response.json()
hours_12_list = weather_data["hourly"][:12]
hours_12_weather_code = [i["weather"][0]["id"] for i in hours_12_list]
print(hours_12_weather_code)
is_rain = False
for i in hours_12_weather_code:
    if i < 700:
        is_rain = True

proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = 'TWILIO_SID'
auth_token = 'TWILIO_TOKEN'
client = Client(account_sid, auth_token, http_client=proxy_client)

if is_rain:
    message = client.messages.create(body="Bring your Umbrella. Its going to rain.", from_='+TWILIO_NUMBER',
                                     to='NUMBER_TO_SEND')
    print(message.sid)
