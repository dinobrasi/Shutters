from flask import Flask, render_template, request, send_from_directory
#from functions import getPublicIP
#from netifaces import interfaces, ifaddresses, AF_INET

#def getPublicIP(which):
#    # either eth0, or wlan0
#    for ifaceName in interfaces():
#        if which == ifaceName:
#            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
#    return ' '.join(addresses)

app = Flask(__name__)

#net = "eth0"
#net = "wlan0"
#public_ip = getPublicIP(net) # '192.168.0.82'
#print(public_ip)

@app.route('/')
def index():
    return send_from_directory("templates", "index.html")

if __name__ == '__main__':

    try:
        app.run('localhost', 80)

    except KeyboardInterrupt:
        endprogram()