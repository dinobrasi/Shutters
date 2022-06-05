from netifaces import interfaces, ifaddresses, AF_INET
from windows import windows

def getWindows():
	buttons = ""
	for window in windows.window_list:
		x = window.split()
		y = "_".join(x).lower()
		buttons = (buttons + 
					"<div class=\"col\"><div class=\"text-center tile windowbg rounded-3\">",
					"<div id=\"" + y + "-up\" class=\"window_top_open windr border border-4 border-bottom-0 rounded-top\"></div>",
					"<div id=\"" + y + "-down\" class=\"window_bot_open windr border border-4 border-top-0 rounded-bottom\"></div>",
					"<div class=\"label\">" + window + "</div></div></div>")
	return buttons

def getPublicIP(which):
	# either eth0, or wlan0
	for ifaceName in interfaces():
		if which == ifaceName:
			addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
	return ' '.join(addresses)