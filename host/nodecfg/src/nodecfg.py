# where is the 485 bus
tty = "/dev/ttyUSB0"
baud = 115200

addr = 1      #current address
naddr = 3     #new address
inputs = 2    #number of input bytes
outputs = 2   #number of output bytes
servos = 2    #number of servo driver boards



import serial
import time

STX  = b'\x02'  # start byte
ETX  = b'\x03'  # end byte
ESC  = b'\x10'  # escape byte

CONFIG = 'F'

def connect(tty, baud):
	port = serial.Serial(port=tty, baudrate=baud, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=5)
	port.dtr = False
	port.rts = False
	time.sleep(2)
	return port
		
def send(port, addr, omsg):
	ob = [0] * len(omsg)
	i = 0
	for byte in omsg:
		ob[i] = byte
		i += 1

	port.write(b'\xFF')
	port.write(b'\xFF')
	port.write(STX)
	port.write(bytes([65 + addr]))
	for byte in ob:
		b = bytes([byte & 0xff])
		if b == ETX:
			port.write(ESC) # escape because this looks like an STX bit (very basic protocol)
		elif b == ESC:
			port.write(ESC) # escape because this looks like an escape bit (very basic protocol)
		port.write(b)

	port.write(ETX)
	port.flush()


port = connect(tty, baud)
cmd = CONFIG + bytes([naddr & 0xff, inputs & 0xff, outputs & 0xff, servos & 0xff])
send(port, addr, cmd)
