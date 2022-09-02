from os import environ
from flask import Flask, render_template, request, send_from_directory
from functions import getWindows
from functions import getPublicIP

app = Flask(__name__)

#net = "eth0"
#net = "wlan0"
#public_ip = getPublicIP(net) # '192.168.0.82'

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
