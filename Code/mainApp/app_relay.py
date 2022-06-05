from os import environ
from flask import Flask, render_template, request, send_from_directory
from functions import getWindows
from functions import getPublicIP

app = Flask(__name__)

#net = "eth0"
net = "wlan0"
public_ip = getPublicIP(net) # '192.168.0.82'

@app.route('/')
def index():
	buttons = getWindows()
	return render_template('default.html', b=buttons)

@app.route("/static/<path:path>")
def static_dir(path):
	return send_from_directory("static", path)

@app.route('/favicon.ico')
def fav():
	return send_from_directory("static", "img/favicon.ico")

if __name__ == '__main__':
	app.run(public_ip, 4450)