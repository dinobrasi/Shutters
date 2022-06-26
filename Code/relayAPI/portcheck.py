import ioexpander
import time

ports = 16

def turnOff(relay):
	cmd = b'e' + bytes(str(relay),'raw_unicode_escape') + b'f'
	ioexpander.SerialCmdDone(cmd)

def turnOn(relay):
	cmd = b'e' + bytes(str(relay),'raw_unicode_escape') + b'o'
	ioexpander.SerialCmdDone(cmd)

def setup():
	print("[Setup] Start")

	ioexpander.ser.flushInput()
	ioexpander.SerialCmdDone(b'eb4')

	print("[Setup] End")

def doLoop():
    for l in range(1, 10):
        for x in range(1, ports + 1):
            print(x)
            turnOn(x)
            time.sleep(.025)
            turnOff(x)

        x = ports - 1
        while x > 0:
            print(x)
            turnOn(x)
            time.sleep(.025)
            
            turnOff(x)
            x = x - 1

if __name__ == "__main__":
	setup()
	doLoop()