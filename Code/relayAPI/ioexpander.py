# IO Expander module v1.0
import serial
import datetime
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=5
    )

# read from the serial port 'until' char is read or 'length' characters received
def SerialReadUntil(cmd, until):
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
        if ch != b'\r':
            bytes += ch
        
    return bytes
     
# bytes to hex bytes     
def btoh2(bytes):
    return bytes.fromhex(bytes.decode("ascii"))

# bytes to long
def btol2(bytes):
    return int(bytes)

# bytes to decimal. ending returned
def btoi2(bytes, start):
    end = start
    while end < len(bytes) and bytes[end] >= ord('0') and bytes[end] <= ord('9'):        
        end += 1
    if (start == end):
        return 0, end
    return int(bytes[start:end]), end+1

# read serial bytes
def SerialReadBytes():
    return SerialReadUntil(None, b'\n')

# read serial int
def SerialReadInt():
    buffer = SerialReadBytes()
    if buffer is not None:
        return btol2(buffer)
    
    return None

def SerialReadHex():
    buffer = SerialReadBytes()
    if buffer is not None:
        return btoh2(buffer)
    
    return None

def SerialReadFloat():
    buffer = SerialReadBytes()
    if buffer is not None:
        if buffer[0] > ord('9'):
            return None
        value = float(buffer.decode('raw_unicode_escape'))
        return value
        
    return None        

# send serial cmd wait for CR returned
def SerialCmd(cmd):
    return SerialReadUntil(cmd, b'\n')

# send serial cmd, wait for '>' returned
def SerialCmdDone(cmd):
    return SerialReadUntil(cmd, b'>')

# wait for '>' returned
def SerialReadUntilDone():
    return SerialReadUntil(None, b'>')

# send serial cmd and check for error returned
def SerialCmdNoError(cmd):
    noerror = False
    
    if SerialCmd(cmd) is not None:
        response = SerialReadBytes()
        if response is not None:
            if response[0] == ord('n'):
                noerror = True

        SerialReadUntilDone()

    return noerror

# send binary serial bitmap using ascii mode
def SerialDisplayBitmap(x, y, w, h, bitmap):
    bw = (w+7)>>3
    size = 0
    ascii = False
    n = 0
    
    for i in range(h):
        if not size:
            ser.write(b'sb')
            ser.write(bytes(str(x),'raw_unicode_escape'))
            ser.write(b',')
            ser.write(bytes(str(y+i),'raw_unicode_escape'))
            ser.write(b',')
            ser.write(bytes(str(w),'raw_unicode_escape'))
            ser.write(b',')
            ascii = False
        for j in range(bw):
            ch = bitmap[n]
            n += 1
            if ch == ord(b'"') or ch == 8 or ch == 13:
                if ascii:
                    ser.write(b'"')
                #if ch < 0x10:
                #    ser.write(b'0')
                ser.write(bytes(hex(ch)[2:].zfill(2),'raw_unicode_escape'))
                if size+j < 99:
                    ser.write(b',')
                ascii = False
            else:
                if not ascii:
                    ser.write(b'"')
                    ascii = True
                ser.write(bytes(chr(ch),'raw_unicode_escape'))
        size += bw
        if i == h-1 or size > 100:
            SerialCmdDone(b'')
            size = 0
            
# serial read time
def SerialReadTime():
    clk = []
    
    if SerialCmd(b'sr') is not None:
        buffer = SerialReadBytes()
        if buffer is not None:
            start = 0
            for _ in range(6):
                value,start = btoi2(buffer, start)
                clk.append(value)
        SerialReadUntilDone()
        dt = datetime.datetime(clk[2]+2000,clk[0],clk[1],clk[3],clk[4],clk[5],0)
        tm = time.localtime(dt.timestamp())
        return tm
        
    return None

# serial write time
def SerialWriteTime(clk):
    ser.write(b'sc')
    ser.write(bytes(str(clk.tm_mon),'raw_unicode_escape'))
    ser.write(b'/')
    ser.write(bytes(str(clk.tm_mday),'raw_unicode_escape'))
    ser.write(b'/')
    ser.write(bytes(str(clk.tm_year-2000),'raw_unicode_escape'))
    ser.write(b' ')
    ser.write(bytes(str(clk.tm_hour),'raw_unicode_escape'))
    ser.write(b':')
    ser.write(bytes(str(clk.tm_min),'raw_unicode_escape'))
    ser.write(b':')
    ser.write(bytes(str(clk.tm_sec),'raw_unicode_escape'))
    return SerialCmdDone(b'')

# serial read EEPROM
def SerialReadEEPROM(address, length):
    size = 16
    data = b''

    while length:
        if size > length:
            size = length
        ser.write(b'sr')
        ser.write(bytes(hex(address)[2:].zfill(4),'raw_unicode_escape'))
        ser.write(bytes(hex(size)[2:].zfill(2),'raw_unicode_escape'))
        SerialCmd(b'')
        buffer = SerialReadBytes()
        SerialReadUntilDone()
        data += btoh2(buffer)
        address += size
        length -= size
        
    return data    

# serial write EEPROM using ascii mode
def SerialWriteEEPROM(data, address):
    size = 0
    ascii = False
    n = 0
    
    length = len(data)
    while length:
        if not size:
            ser.write(b'sw')
            ser.write(bytes(hex(address)[2:].zfill(4),'raw_unicode_escape'))
            ascii = False
        ch = data[n]
        n += 1
        if ch == ord(b'"') or ch == 8 or ch == 13:
            if ascii:
                ser.write(b'"')
            ser.write(bytes(hex(ch)[2:].zfill(2),'raw_unicode_escape'))
            if length > 1 and size < 99:
                ser.write(b',')
            ascii = False
        else:
            if not ascii:
                ser.write(b'"')
                ascii = True
            ser.write(bytes(chr(ch),'raw_unicode_escape'))
        address += 1
        length -= 1
        size += 1
        if not length or size > 100:
            SerialCmdDone(b'')
            size = 0
           
    return True
    
# serial read button
def SerialReadButton(cmd):
    n = 0
    
    SerialCmd(cmd)
    n = SerialReadInt()
    SerialReadUntilDone()
    
    return n

# serial write relay expander using ascii mode
def SerialWriteRelayExpander(data):
    ascii = False
    n = 0
    
    length = len(data)
    ser.write(b'es')
    while length:
        ch = data[n]
        n += 1
        if ch == ord(b'"') or ch == 8 or ch == 13:
            if ascii:
                ser.write(b'"')
            ser.write(bytes(hex(ch)[2:].zfill(2),'raw_unicode_escape'))
            if length > 1:
                ser.write(b',')
            ascii = False
        else:
            if not ascii:
                ser.write(b'"')
                ascii = True
            ser.write(bytes(chr(ch),'raw_unicode_escape'))
        length -= 1

    return SerialCmdDone(b'')