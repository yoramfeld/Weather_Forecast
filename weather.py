# -*- coding: utf-8 -*-
"""weather.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/yoramfeld/Weather_Forecast/blob/main/weather.ipynb
"""

import requests
from datetime import datetime, timezone
api_key='7f0804cb4aab571b1c8921f4d82e1815' #api key for open weather map site
show_line=0 #to handle multi appearnces of a city
city_name=input ("Enter city name: ") #e.g. 'Birmingham' #'Saint Petersburg' #'Jerusalem' #London
location=requests.get('http://api.openweathermap.org/geo/1.0/direct?q='+city_name+'&limit=50&appid='+api_key)

no_of_cities_in_that_name = len(location.json()) #allow handling multi appearances
if no_of_cities_in_that_name==0: #empty response
  print ("City not found")
else:
  #print (location.json())  for debugging
  if no_of_cities_in_that_name > 1: #allow choosing one of a list
    print (f"\nIdentified {no_of_cities_in_that_name} cities under {city_name}")
    for num in range (len(location.json())):
      current=location.json()[num]
      state = '' if not 'state' in current else current['state'] # Protect from no state. e.g. several Hiroshima instances have no state
      print (f"{num+1}. {state} ({current['country']}) at {current['lon']} & {current['lat']}") #list the multi cities

    while True:
      inp_str=(f"Pick between 1 and {len(location.json())}:")
      line_no=int(input (inp_str)) #ask to pick one from the list
      if 0 < line_no <= len(location.json()): #protect from illegal entered values
        break
    show_line=int(line_no)-1 #mark the list element to show

  current=location.json()[show_line]
  state = '' if not 'state' in current else current['state'] # Protect from no state. e.g. several Hiroshima instances have no state
  print (f"\n{city_name} of {state} ({current['country']}) is at {current['lon']} & {current['lat']}")
  w=requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+str(current['lat'])+'&lon='+str(current['lon'])+'&units=metric'+'&appid='+api_key) #read weather info
  main=w.json()['main']
  weather=w.json()['weather'][0]
  print (f"and currently has {main['temp']} degC and {main['humidity']}% humidity with {weather['description']}")
  remote_timestamp=datetime.fromtimestamp(w.json()['dt']+w.json()['timezone']) #use time info in the response
  print ("At",remote_timestamp.strftime("%H:%M"),"on",remote_timestamp.strftime("%d/%m"),"\n")
  print ("Your local date & time is:",datetime.now().strftime("%H:%M"),"on",datetime.now().strftime("%d/%m")) #print the local time and date