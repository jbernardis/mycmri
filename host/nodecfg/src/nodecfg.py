#!/usr/bin/env python3

import sys, getopt
import serial
import time

def usage(msg=None):
	if msg:
		print("%s\n" % msg)
		
	print("usage:\n")
	print("  %s <options> currentaddr newaddr inputs outputs servos\n" % sys.argv[0])
	print("")
	print("  Options:")
	print("    -t or --tty ttyname               the tty devive used to connect to the rs485 bus (/dev/ttyUSB0)")
	print("    -b or --baud baudrate             the baud rate used (115200)")
	print("")
	print("  Positional parameters (all are required):")
	print("    currentaddr                       the current address value configured in the node")
	print("    newaddr                           the new address to be configured into the node")
	print("    inputs                            the number of input bytes");
	print("    outputs                           the number of output bytes");
	print("    servos                            the number of servo/turnout control boards");

try:
	opts, args = getopt.getopt(sys.argv[1:], "ht:b:", ["help", "tty=", "baud="])
except getopt.GetoptError as err:
	print(err)
	usage()
	sys.exit(1)
	
# where is the 485 bus
tty = "/dev/ttyUSB0"
baud = 115200

for o, a in opts:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-t", "--tty"):
		tty = a
	elif o in ("-b", "--baud"):
		try:
			baud = int(a)
		except:
			usage("Unable to parse baud (%s) as an integer value" % a)
			sys.exit(1)
	else:
		usage("Unknown option: %s" % o)
		sys.exit(1)

if len(args) < 5:
	usage("Missing positional parameter(s) - 5 required")
	sys.exit(1)
	
try:
	addr = int(args[0])
except:
	usage("Unable to parse address (%s) as an integer value" % args[0])
	sys.exit(1)
	
try:
	naddr = int(args[1])
except:
	usage("Unable to parse new address (%s) as an integer value" % args[1])
	sys.exit(1)
	
try:
	inputs = int(args[2])
except:
	usage("Unable to parse inputs (%s) as an integer value" % args[2])
	sys.exit(1)
	
try:
	outputs = int(args[3])
except:
	usage("Unable to parse outputs (%s) as an integer value" % args[3])
	sys.exit(1)
try:
	servos = int(args[4])
except:
	usage("Unable to parse servos (%s) as an integer value" % args[4])
	sys.exit(1)

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
