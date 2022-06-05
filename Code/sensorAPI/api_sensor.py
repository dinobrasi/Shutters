# this isn't finished
from flask import Flask, send_from_directory
from functions import getPublicIP

app = Flask(__name__)

#net = "eth0"
net = "wlan0"
public_ip = getPublicIP(net) # '192.168.0.82'
#print(public_ip)

@app.route('/')
def index():
	return send_from_directory("templates", "index.html")

if __name__ == '__main__':
	#try:
	app.run(public_ip, 80)

	#except KeyboardInterrupt:
	#	endprogram()