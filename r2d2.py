import RPi.GPIO as GPIO
import time
import os
import scrollphat
from time import gmtime, strftime
import time
import sys
import subprocess
import bisect
import socket
import sys
import requests
import json
import urllib

#adjust for where your switch is connected

def fuzzy_clock():
	minLookup = [
		' ', 
		'five', 
		'ten', 
		'quarter',
		'twenty',
		'twenty-five',
		'half'
	]
	hourLookup = [
		'midnight',
		'one',
		'two',
		'three',
		'four',
		'five',
		'six',
		'seven',
		'eight',
		'nine',
		'ten',
		'eleven',
		'noon'
	]

	#Get minutes
	time_min = strftime("%M", time.localtime())
	
	#Get hour, as int
	time_hour = int(strftime("%H", time.localtime()))

	#round minutes to nearest 5, return an int
	time_min = int(round(float(time_min)*2, -1)/2)
	print time_min

	
	if time_hour >= 13:
		time_hour = time_hour - 12

	#Get the O'clock for if it's around 0 mins past
	if time_min == 0:
		str_time =  "Its " + hourLookup[time_hour] + " o'clock"
	elif time_min == 60:
		str_time =  "Its " + minLookup[time_min/5] + " past" + hourLoookup[time_hour]
	#if it's less that half past, it;ll be past
	elif time_min <= 30:
		str_time =  "Its " + minLookup[time_min/5] + " past " + hourLookup[time_hour]
	#otherwise it'll be to, you need to invert the minutes and add on an hour
	#    so 35 past 12 becuase 25 to 1
	else:
		str_time =  "Its " + minLookup[(60-time_min)/5] + " to " + hourLookup[time_hour+1]
	return str_time + "   "
	
# Function to give a greeting based on time of the day
def say_greeting(time_hour):
	greeting = " "
	if time_hour >= 0 and time_hour < 5:
		greeting = "Its Too early Nayan"
	elif time_hour >= 5 and time_hour < 12:
		greeting = "Good Morning Nayan"
	elif time_hour >= 12 and time_hour < 17:
		greeting = "Good afternoon Nayan"
	elif time_hour >= 17 and time_hour < 20:
		greeting = "Good evening Nayan"
	elif time_hour >= 20 and time_hour < 22:
		greeting = "Good Night Nayan"
	else:
		greeting = "Looks like you should be in Bed Nayan"

	subprocess.call(['espeak', '-s 150', greeting])
	

#should play a random R2D2 sound
def play_sound(type):
	if type == "clock":
		subprocess.call(["aplay",  "./sounds/R2D2a.wav"])
	elif type == "weather":
		subprocess.call(["aplay", "./sounds/R2D2b.wav"])
	else :
		subprocess.call(["aplay","./sounds/r2d2wst4.wav"])
		


# requires: netifaces for looking up IP in readable way
# requires: requests human readable HTTP requests

def get_location():
    res = requests.get('http://ipinfo.io')
    if(res.status_code == 200):
        json_data = json.loads(res.text)
        return json_data
    return {}


# Python 2 vs 3 breaking changes.
def encode(qs):
    val = ""
    try:
        val = urllib.urlencode(qs).replace("+","%20")
    except:
        val = urllib.parse.urlencode(qs).replace("+", "%20")
    return val

def get_weather(address):
    base = "https://query.yahooapis.com/v1/public/yql?"
    query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\""+address+"\") and u='c'"
    print query
    qs={"q": query, "format": "json", "env": "store://datatables.org/alltableswithkeys"}

    uri = base + encode(qs)                                        

    res = requests.get(uri)
    if(res.status_code==200):
        json_data = json.loads(res.text)
        return json_data
    return {}

#get message to display 

def say_clock():
	play_sound("clock")
	current = fuzzy_clock()
	subprocess.call(['espeak', '-s 150', current])
	print current
	return current

def say_date():
	play_sound("clock")
	current =  strftime("Today is %A %-d of %B %Y")
	subprocess.call(['espeak', '-s 150', current])
	current = strftime(" %a, %-d %b %Y ", time.localtime())
	return current

def say_weather():
	play_sound("weather")
	location = get_location()
	location_string = location["city"] +", " + location["country"]
	print("Location: " + location_string)
	output = location_string + " "

	if(location["city"] != None):
		weather = get_weather(location_string)

	# Feel free to pick out other data here, for the scrolling message
	for x in range(0, 2):
		item = weather["query"]["results"]["channel"]["item"]["forecast"][x]
		output_speak = "The weather in " + location["city"] + "is " + item["text"] +  "low of " + item["low"] +" degree celsius and high of " + item["high"] + " degree celsius"
		output = output + item["day"] +": " + item["text"] + " - L: "+ item["low"] + "C - H: "+ item["high"]+"C "

		#subprocess.call(['espeak',  '-s 150', output_speak])

		return output
	

#adjust for where your switch is connected
def led_status(buttonPin):
	global option, RED, YELLOW, BLUE, GREEN, LED
	if GPIO.input(buttonPin) == GPIO.HIGH:

		print ("LED OFF")
	else:
		print ("LED ON")
		time_hour = int(strftime("%H", time.localtime()))
		say_greeting(time_hour)
		if option == 1:
			LED = GREEN
			current = say_clock()
			cur_time = strftime("%H:%M", time.localtime())

			current =  cur_time + "     " + current

		elif option == 2:
			LED=RED
			current = say_date()

		elif option == 3:
			LED = YELLOW
			current = say_weather() 

		print current

		scrollphat.set_brightness(4)
		while True:
		    try:
			GPIO.output(LED, GPIO.HIGH)
			scrollphat.write_string(current ) 
			scrollphat.scroll()
			time.sleep(0.1)
			GPIO.output(LED, GPIO.LOW)
			if GPIO.input(buttonPin) == GPIO.HIGH:
				raise KeyboardInterrupt()
		    except KeyboardInterrupt:
			play_sound("stop")
			scrollphat.clear()
			GPIO.output(LED, GPIO.LOW)
			option += 1
			if option > 3:
				option = 1

			return
			#sys.exit(-1)


# Pin detecting the LED
buttonPin = 17
option = 1
# LED's
RED = 27
BLUE = 23
GREEN = 24
YELLOW = 22
#Show's which light should be on
LED = RED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)


GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=led_status, bouncetime=5000)
while True:
	#assuming that the script to call is long enough we can ignore bouncing
	time.sleep(0.02)

