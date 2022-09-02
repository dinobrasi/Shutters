#!/usr/bin/env python
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from functions import getPublicIP

import sys
import time

import ioexpander

app = Flask(__name__)
api = Api(app)

#net = "eth0"
#net = "wlan0"
#public_ip = getPublicIP(net)

#net = "eth0"
net = "wlan0"
expected_ip = "192.168.0.230" # waiting for the network at boot. I know there is a setting, but it wasn't working for me.
waiting = True
counter = 0

while waiting:
    public_ip = getPublicIP(net)
    
    sys.stdout.write("[" + str(counter) + "] Waiting for IP Address " + expected_ip + ". Getting: " + public_ip + "\r")
    sys.stdout.flush()

    if expected_ip == public_ip:
        waiting = False
    else:
        counter = counter + 1
        
        if counter == 1000:
            waiting = False 
    
    time.sleep(1) # waiting for the network at boot. I know there is a setting, but it wasn't working for me.

window_list = {
	"window_1" : { "board": 2, "down": 17, "up": 18 },
	"window_2" : { "board": 2, "down": 19, "up": 20 },
	"window_3" : { "board": 2, "down": 21, "up": 22 },
	"window_4" : { "board": 2, "down": 23, "up": 24 },
	"window_5" : { "board": 2, "down": 25, "up": 26 },
	"window_6" : { "board": 2, "down": 27, "up": 28 },
	"window_7" : { "board": 2, "down": 29, "up": 30 },
	"window_8" : { "board": 2, "down": 31, "up": 32 },
	"window_9" : { "board": 1, "down": 1, "up": 2 },
	"window_10" : { "board": 1, "down": 3, "up": 4 },
	"window_11" : { "board": 1, "down": 5, "up": 6 },
	"window_12" : { "board": 1, "down": 7, "up": 8 },
	"window_13" : { "board": 1, "down": 9, "up": 10 },
	"window_14" : { "board": 1, "down": 11, "up": 12 },
	"window_15" : { "board": 1, "down": 13, "up": 14 },
	"window_16" : { "board": 1, "down": 15, "up": 16 },
	"window_17" : { "board": 3, "down": 1, "up": 2 },
	"window_18" : { "board": 3, "down": 3, "up": 4 },
	"window_19" : { "board": 3, "down": 5, "up": 6 },
	"window_20" : { "board": 3, "down": 7, "up": 8 },
	"window_21" : { "board": 3, "down": 9, "up": 10 },
	"window_22" : { "board": 3, "down": 11, "up": 12 },
	"window_23" : { "board": 3, "down": 13, "up": 14 },
	"window_24" : { "board": 3, "down": 15, "up": 16 },
	"window_25" : { "board": 4, "down": 17, "up": 18 },
	"window_26" : { "board": 4, "down": 19, "up": 20 },
	"window_27" : { "board": 4, "down": 21, "up": 22 },
	"window_28" : { "board": 4, "down": 23, "up": 24 },
	"window_29" : { "board": 4, "down": 25, "up": 26 },
	"window_30" : { "board": 4, "down": 27, "up": 28 },
	"window_31" : { "board": 4, "down": 29, "up": 30 },
	"window_32" : { "board": 4, "down": 31, "up": 32 },
}

@app.route("/")
def home():
	return render_template('index.html')

def turnOff(relay):
	cmd = b'e' + bytes(str(relay),'raw_unicode_escape') + b'f'
	ioexpander.SerialCmdDone(cmd)

def turnOn(relay):
	cmd = b'e' + bytes(str(relay),'raw_unicode_escape') + b'o'
	ioexpander.SerialCmdDone(cmd)

class Window(Resource):
	def get(self):
		return window_list

class WindowID(Resource):
	def get(self, window_id, direction, status):
		window_name = 'window_'+window_id
		thisWindow = window_list[window_name]
		
		if direction == "down":
			relay_id = thisWindow["down"]
		else:
			relay_id = thisWindow["up"]

		if status == "on":
			turnOn(relay_id)
		else:
			turnOff(relay_id)

		return {'window_id': window_id, "direction": direction, "window_name": window_name, "relay_id": relay_id }

def setup():
	print("[Setup] Start")

	CORS(app)

	ioexpander.ser.flushInput()
	ioexpander.SerialCmdDone(b'eb4')

	api.add_resource(Window, '/window/')
	api.add_resource(WindowID, '/window/<window_id>/<direction>/<status>')

	print("[Setup] End")

if __name__ == "__main__":
	setup()
	print("public ip:", public_ip)
	app.run(public_ip, 4449)
