#!/usr/bin/env python

import scrollphat
from time import gmtime, strftime
import time
import sys
import bisect


def fuzzy_clock():
	minLookup = [
		' ', 
		'five', 
		'ten', 
		'quarter',
		'twenty',
		'twenty-five'
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

	
	if time_hour >= 13:
		time_hour = time_hour - 12

	#Get the O'clock for if it's around 0 mins past
	if time_min == 0:
		str_time =  "It's " + hourLookup[time_hour] + " o'clock"
	elif time_min == 60:
		str_time =  "It's " + minLookup[time_min/5] + " past" + hourLoookup[time_hour]
	#if it's less that half past, it;ll be past
	elif time_min <= 30:
		str_time =  "It's " + minLookup[time_min/5] + " past " + hourLookup[time_hour+1]
	#otherwise it'll be to, you need to invert the minutes and add on an hour
	#    so 35 past 12 becuase 25 to 1
	else:
		str_time =  "It's " + minLookup[(60-time_min)/5] + " to " + hourLookup[time_hour+1]
	return str_time + "   "
	

current = fuzzy_clock()
cur_time = strftime("%H:%M", time.localtime())

current =  cur_time + "     " + current
print current
scrollphat.set_brightness(4)
while True:
    try:
	scrollphat.write_string(current ) 
	scrollphat.scroll()
        time.sleep(0.3)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)


# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.
