OUTPUT_ON = b'1'
OUTPUT_OFF = b'0'
OUTPUT_CURRENT = b'O'
INPUT_DELTA = b'D'
INPUT_CURRENT = b'C'
TURNOUT_NORMAL = b'N'
TURNOUT_REVERSE = b'R'
IDENTIFY = b'Y'
SERVO_ANGLE = b'A'
SET_TURNOUT = b'T'
GET_TURNOUT = b'G'
CONFIG = b'F'
ACKNOWLEDGE = b'!'
STORE = b'W'
ERRORRESPONSE = b'E'

def commandName(cmd):
	if cmd == OUTPUT_ON:
		return("OUTPUT_ON")
	elif cmd == OUTPUT_OFF:
		return("OUTPUT_OFF")
	elif cmd == OUTPUT_CURRENT:
		return("OUTPUT_CURRENT")
	
	elif cmd == INPUT_DELTA:
		return("INPUT_DELTA")
	elif cmd == INPUT_CURRENT:
		return("INPUT_CURRENT")
	
	elif cmd == TURNOUT_NORMAL:
		return("TURNOUT_NORMAL")
	elif cmd == TURNOUT_REVERSE:
		return("TURNOUT_REVERSE")
	elif cmd == SERVO_ANGLE:
		return("SERVO_ANGLE")
	elif cmd == SET_TURNOUT:
		return("SET_TURNOUT")
	elif cmd == GET_TURNOUT:
		return("GET_TURNOUT")
	
	elif cmd == IDENTIFY:
		return("IDENTIFY")
	elif cmd == CONFIG:
		return("CONFIG")
	elif cmd == ACKNOWLEDGE:
		return("ACKNOWLEDGE")
	elif cmd == STORE:
		return("STORE")
	elif cmd == ERRORRESPONSE:
		return("ERRORRESPONSE")
	
	else:
		return("UNKNOWN COMMAND: %s" % str(cmd))
