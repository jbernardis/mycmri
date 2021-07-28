// Still To Do
//
// multiple nodes
// design board for rpi 

#include <EEPROM.h>

#include <SimpleTimer.h>
SimpleTimer timer;

#include "inputboard.h"
#include "outputboard.h"
#include "servodriver.h"
#include "display.h"
#include "rs485.h"
#include "button.h"

int _address = 2;
int _i_chips = 2;
int _o_chips = 2;
int _servo_bds = 1;

int ibits;
int obits;
int svbits;

int limitsOffset = 0;

#define BUSBAUD 115200
#define BUSCONFIG SERIAL_8N2
RS485 bus(2); // pin 2 for DE control

// Instantiate the object for  Input Boards
InputBoard inBd(8, 9, 11, 12);

// Instantiate the object for output boards
OutputBoard outBd(5, 6, 7);

// Instantiate the servo driver
ServoDriver servo;

Display disp;

Button bINFO(3, 50);
#define INFO_ADDRESS 0
#define INFO_INPUTS 1
#define INFO_OUTPUTS 2
#define INFO_SERVOS 3
int infoIndex;
int infoMode = INFO_ADDRESS;

int * inputValues;
int * outputPulses;

enum {
	PREAMBLE_1,
	PREAMBLE_2,
	PREAMBLE_3,
	DECODE_ADDR,
	DECODE_CMD,
	DECODE_DATA,
	DECODE_ESC_DATA,
	IGNORE_CMD,
	IGNORE_DATA,
	IGNORE_ESC_DATA,
	POSTAMBLE_SET,
	POSTAMBLE_POLL,
	POSTAMBLE_OTHER
};

enum {
	OUTPUT_ON = '1',
	OUTPUT_OFF = '0',
	OUTPUT_PULSE = 'P',
	OUTPUT_CURRENT = 'O',
	INPUT_DELTA = 'D',
	INPUT_CURRENT = 'C',
	TURNOUT_NORMAL = 'N',
	TURNOUT_REVERSE = 'R',
	IDENTIFY = 'Y',
	SERVO_ANGLE = 'A',
	SET_TURNOUT = 'T',
	GET_TURNOUT = 'G',
	ACKNOWLEDGE = '!',
	CONFIG = 'F',
	STORE = 'W',
	NOOP = 0x00, // do nothing
	STX  = 0x02, // start byte
	ETX  = 0x03, // end byte
	ESC  = 0x10, // escape byte
};

int _mode = PREAMBLE_1;
int _rx_index = 0;
int _rx_length = 8;
char * _rx_buffer;
int _tx_index = 0;
int _tx_length = 0;
char * _tx_buffer;
int _cmd;

int pulsesPerUpdate = 4;
int pulsesTilUpdate = 0;

void(* resetFunc) (void) = 0;

void setup() {
	loadConfig();
	ibits = _i_chips * 8;
	obits = _o_chips * 8;
	svbits = _servo_bds * 16;
	disp.nodeConfig(_address, _i_chips, _o_chips, _servo_bds);
	disp.begin();
	disp.showConfig();

	pinMode(LED_BUILTIN, OUTPUT);

	int _tx_l1 = ibits * 2; // one for each input bit plus its index - worst case
	int _tx_l2 = svbits * 4; // normal, reverse, initial, current for each servo
	int _tx_l3 = obits;
	
	_tx_length = max(max(_tx_l1, _tx_l2), _tx_l3);

	_rx_buffer = (char *) malloc(_rx_length);
	_tx_buffer = (char *) malloc(_tx_length);

	bus.begin(BUSBAUD, BUSCONFIG);
	timer.setInterval(250, pulse);

	inputValues = (int *) malloc(ibits * sizeof(int));
	outputPulses = (int *) malloc(obits * sizeof(int));
	inBd.setup(_i_chips);
 	outBd.setup(_o_chips);
	servo.setup(_servo_bds);

	loadLimits();

	servo.initialPositions();

	// retrieve initial switch positions
	inBd.retrieve();
	for (int i=0; i<ibits; i++) {
		*(inputValues+i) = inBd.getBit(i);
	}
	// initially set all output pulses to 0
	for (int i=0; i<obits; i++) {
		*(outputPulses+i) = 0;
	}
	bINFO.begin();
}

void loop() {
	timer.run();
}

void pulse() {
	int norm, rev, ini, curr;

	inBd.retrieve();
	pulsedOutputs();

	pulsesTilUpdate--;
	if (pulsesTilUpdate <= 0) {
		pulsesTilUpdate = pulsesPerUpdate;
		if (disp.update()) {
			infoMode = INFO_ADDRESS;
			infoIndex = 0;
		}
	}

	if (bINFO.pressed()) {
		switch (infoMode) {
			case INFO_ADDRESS:
				disp.showConfig();
				infoMode = INFO_INPUTS;
				infoIndex = 0;
				break;

			case INFO_INPUTS:
				if (_i_chips == 0) {
					disp.message("No in chips");
				}
				else {
					int cv = inBd.getChip(infoIndex);
					disp.showInputChip(infoIndex, cv);
					infoIndex++;
				}
				
				if (infoIndex >= _i_chips) {
					infoMode = INFO_OUTPUTS;
					infoIndex = 0;
				}
				break;

			case INFO_OUTPUTS:
				if (_o_chips == 0) {
					disp.message("No out chips");
				}
				else {
					int cv = outBd.getChip(infoIndex);
					disp.showOutputChip(infoIndex, cv);
					infoIndex++;
				}
				
				if (infoIndex >= _o_chips) {
					infoMode = INFO_SERVOS;
					infoIndex = 0;
				}
				break;

			case INFO_SERVOS:
				if (svbits == 0) {
					disp.message("No servo drivers");
				}
				else {
					if (servo.getConfig(infoIndex, &norm, &rev, &ini, &curr))
						disp.showServo(infoIndex, norm, rev, ini, curr);
					else
						disp.message("ERR servo");
					infoIndex++;				
				}
				
				if (infoIndex >= svbits) {
					infoMode = INFO_ADDRESS;
					infoIndex = 0;
				}
				break;

			default:
				disp.message("Unknown info state");
				break;
		}
	}
}

void serialEvent() {
    while (bus.available()) {
    	if (process_char(bus.read()))
    		return;
    }
}

void pulsedOutputs(void) {  
  for (int i = 0; i<obits; i++) {
    if (*(outputPulses+i) < 0) {
      *(outputPulses+i) = - *(outputPulses+i);
      outBd.setBit(i);
      outBd.send();
      disp.pulseOn(i, *(outputPulses*i));       
    }
    else if (*(outputPulses+i) > 0) {
      *(outputPulses+i) = *(outputPulses+i)-1;
      if (*(outputPulses+i) == 0) {
        outBd.clearBit(i);
        outBd.send();
        disp.pulseOff(i);       
      }
    }
  }
}

bool process_char(char c) {
	uint8_t cmd = decode(c);
 
	switch (cmd) {
	case OUTPUT_ON:
		if (_rx_index > 0) {
			int ox = (int) _rx_buffer[0];
			outBd.setBit(ox);
			outBd.send();
			disp.outputOn(ox);
		}
		acknowledge();
		break;

	case OUTPUT_PULSE:
		if (_rx_index > 0) {
			int ox = (int) _rx_buffer[0];
			int pl = 1;
			if (_rx_index > 1)
				pl = (int) _rx_buffer[1];

			*(outputPulses+ox) = -pl;
		}
		acknowledge();
		break;

	case OUTPUT_OFF:
		if (_rx_index > 0) {
			int ox = (int) _rx_buffer[0];
			outBd.clearBit(ox);
			outBd.send();
			disp.outputOff(ox);
		}
		acknowledge();
		break;
    	
    case OUTPUT_CURRENT:
    	outputCurrent();
    	break;
		
    case TURNOUT_NORMAL:
		if (_rx_index > 0) {
	    	int tx = (int) _rx_buffer[0];
	    	servo.setNR(tx, 1);
			disp.turnoutNormal(tx);
		}
		acknowledge();
		break;

	case TURNOUT_REVERSE:
		if (_rx_index > 0) {
	    	int tx = (int) _rx_buffer[0];
	    	servo.setNR(tx, 0);
			disp.turnoutReverse(tx);
		}
		acknowledge();
		break;

    case INPUT_DELTA:
    	inputDeltas();
    	break;
    	
    case INPUT_CURRENT:
    	inputCurrent();
    	break;
    	
    case IDENTIFY:
    	identify();
    	disp.showConfig();
    	break;
    	
    case SERVO_ANGLE:
		if (_rx_index > 1) {
			int sv = (int) _rx_buffer[0];
			int angle = (int) _rx_buffer[1];
			
			servo.setValue(sv, angle);
			disp.servoAngle(sv, angle);
		}
		acknowledge();
		break;

	case GET_TURNOUT:
		servosConfig();
		break;

    case SET_TURNOUT:
    	if (_rx_index > 2) {
    		int sv = (int) _rx_buffer[0];
    		int n = (int) _rx_buffer[1];
    		int r = (int) _rx_buffer[2];
    		int i;
    		if (_rx_index > 3)
    			i = (int) _rx_buffer[3];
    		else
    			i = n;

			servo.setLimits(sv, n, r);
			servo.setInitialPosition(sv, i);
		}
		acknowledge();
    	break;

    case CONFIG:
    	if (_rx_index > 3) {
    		_address = (int) _rx_buffer[0];
    		_i_chips = (int) _rx_buffer[1];
    		_o_chips = (int) _rx_buffer[2];
 			_servo_bds = (int) _rx_buffer[3];
 			storeConfig();
 			resetFunc();
 		}
		acknowledge();
    	break;

	case STORE:
		storeConfig();
		disp.message("Limits stored");
		acknowledge();
		break;
		
	default:
		return false;
	}
   	return true;
}

uint8_t decode(uint8_t c) {
    switch(_mode) {
        case PREAMBLE_1:
            _rx_index = 0;
            if (c == 0xFF) {
                _mode = PREAMBLE_2;
            }
            break;

        case PREAMBLE_2:
            if (c == 0xFF) {
                _mode = PREAMBLE_3;
            }
            else {
                _mode = PREAMBLE_1;
            }
            break;

        case PREAMBLE_3:
            if (c == STX) {
                _mode = DECODE_ADDR;
            }
            else {
                _mode = PREAMBLE_1;
            }
            break;

        case DECODE_ADDR:
            if (c == 'A' + _address) {
                _mode = DECODE_CMD;
            }
            else if (c >= 'A') {
                _mode = IGNORE_CMD;
            }
            else {
                _mode = PREAMBLE_1;
            }
            break;

        case DECODE_CMD:
        	_cmd = c;
			_mode = DECODE_DATA;
            break;

        case IGNORE_CMD:
            _mode = IGNORE_DATA;
            break;

        case DECODE_DATA:
            if (c == ESC) {
                _mode = DECODE_ESC_DATA;
            }
            else if (c == ETX) {
       			_mode = PREAMBLE_1;
        		return _cmd;
            }
            else if (_rx_index < _rx_length) {
                _rx_buffer[_rx_index++] = c;
            }
            break;

        case DECODE_ESC_DATA:
            if (_rx_index < _rx_length) {
                _rx_buffer[_rx_index++] = c;
            }
            _mode = DECODE_DATA;
            break;

        case IGNORE_DATA:
            if (c == ESC) {
                _mode = IGNORE_ESC_DATA;
            }
            else if (c == ETX) {
       			_mode = PREAMBLE_1;
        		return NOOP;
            }
            break;

        case IGNORE_ESC_DATA:
            _mode = IGNORE_DATA;
            break;

        case POSTAMBLE_OTHER:
            _mode = PREAMBLE_1;
            break;
    }
    return NOOP;
}

void inputDeltas() {
	_tx_index = 0;
	for (int i=0; i<ibits; i++) {
		int bv = inBd.getBit(i);
		if (bv != *(inputValues+i)) {
			if (_tx_index < _tx_length-1) {
				_tx_buffer[_tx_index++] = i;
				_tx_buffer[_tx_index++] = bv;
			}
			*(inputValues+i) = bv;
		}
	}
   	transmit(INPUT_DELTA);
}

void inputCurrent() {
	_tx_index = 0;
	for (int i=0; i<ibits; i++) {
		int bv = inBd.getBit(i);
		if (_tx_index < _tx_length) {
			_tx_buffer[_tx_index++] = bv;
		}
		*(inputValues+i) = bv;
	}
   	transmit(INPUT_CURRENT);
}


void outputCurrent() {
	_tx_index = 0;
	for (int i=0; i<obits; i++) {
		int bv = outBd.getBit(i);
		if (_tx_index < _tx_length) {
			_tx_buffer[_tx_index++] = bv;
		}
	}
   	transmit(OUTPUT_CURRENT);
}

void servosConfig() {
	_tx_index = 0;
	for (int i=0; i<svbits; i++) {
		int norm, rev, ini, current;

		servo.getConfig(i, &norm, &rev,  &ini, &current);
		
		if (_tx_index < _tx_length-3) {
			_tx_buffer[_tx_index++] = norm;
			_tx_buffer[_tx_index++] = rev;
			_tx_buffer[_tx_index++] = ini;
			_tx_buffer[_tx_index++] = current;
		}
	}
	transmit(GET_TURNOUT);
}

void identify() {
	_tx_buffer[0] = _address;
	_tx_buffer[1] = _i_chips;
	_tx_buffer[2] = _o_chips;
	_tx_buffer[3] = _servo_bds;
	_tx_index = 4;
	transmit(IDENTIFY);
}

void acknowledge() {
	_tx_index = 0;
	transmit(ACKNOWLEDGE);
}

void transmit(char cmd) {
    delay(50); // tiny delay to let things recover
    bus.write(255);
    bus.write(255);
    bus.write(STX);
    bus.write(65 + _address);
    bus.write(cmd);
    for (int i=0; i<_tx_index; i++)
    {
        if (_tx_buffer[i] == ETX)
            bus.write(ESC); 
        if (_tx_buffer[i] == ESC)
            bus.write(ESC); 
        bus.write(_tx_buffer[i]);
    }
    bus.write(ETX);
    bus.flush();
}

#define SIGBYTE0 't'
#define SIGBYTE1 'c'
#define GENERATION 4

void loadConfig() {
	limitsOffset = -1;
	int offset = 0;
    if (EEPROM.read(offset++) != SIGBYTE0) {
        return;
    }
    if (EEPROM.read(offset++) != SIGBYTE1) {
        return;
    }
    if (EEPROM.read(offset++) != GENERATION) {
        return;
    }

    _address = EEPROM.read(offset++);
    _i_chips = EEPROM.read(offset++);
    _o_chips = EEPROM.read(offset++);
    _servo_bds = EEPROM.read(offset++);
    limitsOffset = offset;	
}

void loadLimits() {
	if (limitsOffset < 0)
		return;
		
    int offset = limitsOffset;
	
	int nh = EEPROM.read(offset++);
	int nl = EEPROM.read(offset++);
	
	int nlimits = nh * 256 + nl;
	int nservos = servo.getNServos();
	if (nservos < nlimits)
		nlimits = nservos;
	
	for (int i=0; i<nlimits; i++) {
		nh = EEPROM.read(offset++);
		nl = EEPROM.read(offset++);
		int norm = nh*256 + nl;
		
		nh = EEPROM.read(offset++);
		nl = EEPROM.read(offset++);
		int rev = nh*256 + nl;
		
		nh = EEPROM.read(offset++);
		nl = EEPROM.read(offset++);
		int pos = nh*256 + nl;
		
		servo.setLimits(i, norm, rev);
		servo.setInitialPosition(i, pos);
	}  
}

void storeConfig() {
    int offset = 0;
    EEPROM.update(offset++, SIGBYTE0);
    EEPROM.update(offset++, SIGBYTE1);
    EEPROM.update(offset++, GENERATION);

    EEPROM.update(offset++, _address);
    EEPROM.update(offset++, _i_chips);
    EEPROM.update(offset++, _o_chips);
    EEPROM.update(offset++, _servo_bds);

    int n = servo.getNServos();
    EEPROM.update(offset++, n/256);
    EEPROM.update(offset++, n%256);

    for (int i = 0; i<n; i++) {
		int norm, rev;
		if (servo.getLimits(i, &norm, &rev)) {
			EEPROM.update(offset++, norm/256);
			EEPROM.update(offset++, norm%256);
			EEPROM.update(offset++, rev/256);
			EEPROM.update(offset++, rev%256);
		}

		int pos = servo.getInitialPosition(i);
		if (pos >= 0) {
			EEPROM.update(offset++, pos/256);
			EEPROM.update(offset++, pos%256);
		}
    }
}
