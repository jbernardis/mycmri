import time

from cmri import CMRI, CMRI_READ_EXCEPTION, CMRI_COMMAND_EXCEPTION, CMRI_ADDRESS_EXCEPTION

import serial
from serial import rs485

def processInput(bitx, nv):
	print("input bit %d has changed to %d" % (bitx, nv))

#ser = serial.Serial(port="/dev/ttyUSB0", baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, rtscts=True, dsrdtr=True, timeout=5)
ser = serial.rs485.RS485(port="/dev/ttyUSB1", baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=5)
ser.rs485_mode = serial.rs485.RS485Settings()

c = CMRI(0, ser, processInput)

#while(True):
	#try:
		#c.process()
	#except CMRI_READ_EXCEPTION:
		#print("read exception")
	#except CMRI_COMMAND_EXCEPTION as e:
		#print("Unexpected command in input: %c" % e.badcmd)
	#except CMRI_ADDRESS_EXCEPTION as e:
		#print("Input address %d does not match expected address %d" % (e.badaddr, e.addr))

	#time.sleep(0.25)
c.process()

time.sleep(5)

c.setOutputBit(1, 1);
c.process()

ser.close()
