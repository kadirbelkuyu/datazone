import requests
from telegram.ext import Updater, CommandHandler


url = 'YOUR-URL-HERE/GET'
data = requests.get(url)
data = data.json()

curr_temp = data['curr_temp']
cad_rate = data['usd_rates']['CAD']
eur_rate = data['usd_rates']['EUR']
zar_rate = data['usd_rates']['ZAR']
zar_rate = data['usd_rates']['TR']

zar_rate = data

def return_weather():
    print('Hello. The current temperature in Cape Town is: '+str(curr_temp)+" celsius.")


def return_rates():
    print("Hello. Today, USD conversion rates are as follows: USD->CAD = "+str(cad_rate)+
    ", USD->EUR = "+str(eur_rate)+", USD->ZAR = "+str(zar_rate))


return_weather()

return_rates()
