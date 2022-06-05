# this isn't finished
import json
import serial
import time

from functions import getPublicIP
#from multiprocessing import Process

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

ser.flushInput()

#net = "eth0"
net = "wlan0"
public_ip = getPublicIP(net) # '192.168.0.82'
print(public_ip)

up = "up"
down = "down"
middle = "middle"

sensor_position = {
    "sensor_1" : { "state": "up" },
    "sensor_2" : { "state": "up" },
    "sensor_3" : { "state": "up" },
    "sensor_4" : { "state": "up" },
    "sensor_5" : { "state": "up" },
    "sensor_6" : { "state": "up" },
    "sensor_7" : { "state": "up" },
    "sensor_8" : { "state": "up" }
}

sensor_list = {
    "sensor_1" : { "down": 1, "up": 2 },
    "sensor_2" : { "down": 3, "up": 4 },
    "sensor_3" : { "down": 5, "up": 6 },
    "sensor_4" : { "down": 7, "up": 8 },
    "sensor_5" : { "down": 9, "up": 10 },
    "sensor_6" : { "down": 11, "up": 12 },
    "sensor_7" : { "down": 13, "up": 14 },
    "sensor_8" : { "down": 15, "up": 16 }
}

sensor_1_dn = sensor_list["sensor_1"]["down"]
sensor_1_up = sensor_list["sensor_1"]["up"]
sensor_2_dn = sensor_list["sensor_2"]["down"]
sensor_2_up = sensor_list["sensor_2"]["up"]
sensor_3_dn = sensor_list["sensor_3"]["down"]
sensor_3_up = sensor_list["sensor_3"]["up"]
sensor_4_dn = sensor_list["sensor_4"]["down"] 
sensor_4_up = sensor_list["sensor_4"]["up"]
sensor_5_dn = sensor_list["sensor_5"]["down"]
sensor_5_up = sensor_list["sensor_5"]["up"]
sensor_6_dn = sensor_list["sensor_6"]["down"]
sensor_6_up = sensor_list["sensor_6"]["up"]
sensor_7_dn = sensor_list["sensor_7"]["down"]
sensor_7_up = sensor_list["sensor_7"]["up"]
sensor_8_dn = sensor_list["sensor_8"]["down"]
sensor_8_up = sensor_list["sensor_8"]["up"]

def changePosition(sensor, state):
    sensor_position[sensor]["state"] = state

def xSerialCmd(cmd):
    return xSerialReadUntil(cmd, b'\n')

# wait for '>' returned
def xSerialReadUntilDone():
    return xSerialReadUntil(None, b'>')

# read from the serial port 'until' char is read or 'length' characters received
def xSerialReadUntil(cmd, until):
    bytes = b''
    if cmd is not None:
        ser.write(cmd + b'\r\n')
    while 1:
        ch = ser.read()
        if ch == b'':
            if len(bytes) == 0:
                return None
            break
        if ch == until:
            break

        if ch != b'\r' and ch != b'\n':
            last = ch

    if until == b'>':
        if last == b'0':
            #print("returning False")
            ser.flushInput()
            return False #'closed'
        else:
            #print("returning True")
            #ser.flushInput()
            return True #'open'
    else:
        #ser.flushInput()
        return None
    
def GPIO_input(sensor):
    #print("GPIO_input(", sensor, ")")
    cmd = b'g' + bytes(str(sensor),'raw_unicode_escape') + b'w1;gi'
    #cmd = b'g12w1;gi'
    xSerialCmd(cmd)
    return xSerialReadUntilDone()

def readSensor(sensor):
    #print("Spawning process for", sensor)
    sensor_dn = sensor_list[sensor]["down"]
    sensor_up = sensor_list[sensor]["up"]    
    
    #state_dn_last  = ""
    #state_dn_this  = ""
    #state_up_last  = ""
    #state_up_this  = ""

    state_this = ""
    state_last = ""

    sensor_dn_state = GPIO_input(sensor_dn)
    sensor_up_state = GPIO_input(sensor_up)

    # state change display
    #if sensor_up_state == False:
    #    state_up_this = sensor + " up closed"
    #else:
    #    state_up_this = sensor + " up open"
    #if state_up_last != state_up_this:
    #    print(state_up_this)
    #if sensor_dn_state == False:
    #    state_dn_this = sensor + " dn closed"
    #else:
    #    state_dn_this = sensor + " dn open"
    #if state_dn_last != state_dn_this:
    #    print(state_dn_this)
    
    if sensor_up_state == True & sensor_dn_state == True:
        #print(sensor + " " + middle)
        state_this = middle
    else:
        if sensor_up_state == True:
            #print(sensor + " " + up)
            state_this = up
        else:
            if sensor_dn_state == True:
                #print(sensor + " " + down)
                state_this = down
            else:
                #print(sensor + " " + middle)
                state_this = middle

    #state_up_last = state_up_this
    #state_dn_last = state_dn_this
    
    if state_last != state_this:
        print(sensor + " " + state_this)
        changePosition(sensor, state_this)
        
        j = json.dumps(sensor_position)

        MyFile = open("/home/tim/Documents/Shutter/Sensor/templates/index.html", "w+")
        MyFile.write(j)
        MyFile.close()

    state_last = state_this
        
def setup():
    print("setup")
    ser.flushInput()

def endprogram():
    print("done")
    ser.flushInput()

if __name__ == '__main__':
    setup()

    try:
        while True:
            print("Read...")
            readSensor("sensor_1") # 1-2
            readSensor("sensor_2") # 3-4
            readSensor("sensor_3") # 5-6
            readSensor("sensor_4") # 7-8
            readSensor("sensor_5") # 9-10
            readSensor("sensor_6") # 11-12
            readSensor("sensor_7") # 13-14
            readSensor("sensor_8") # 15-16
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        endprogram()