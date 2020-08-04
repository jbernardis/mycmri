#include <EEPROM.h>
#include <SimpleTimer.h>
SimpleTimer timer;

#include "inputboard.h"
#include "outputboard.h"
#include "servodriver.h"

int _address = 0;
int _i_chips = 2;
int _o_chips = 2;
int _servo_bds = 2;

int ibits;
int obbits;
int svbits;

int limitsOffset = 0;

// Instantiate the object for  Input Boards
InputBoard inBd(8, 9, 11, 12);

// Instantiate the object for output boards
OutputBoard outBd(5, 6, 7);

// Instantiate the servo driver
ServoDriver servo;

int * inputValues;

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
    INPUT_DELTA = 'D',
    INPUT_CURRENT = 'C',
    TURNOUT_NORMAL = 'N',
    TURNOUT_REVERSE = 'R',
    IDENTIFY = 'Y',
    SERVO_ANGLE = 'A',
    SET_TURNOUT = 'T',
    GET_TURNOUT = 'G',
    ACKNOWLEDGE = '!',
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

void setup() {
	ibits = _i_chips * 8;
	obbits = _o_chips * 8;
	svbits = _servo_bds * 16;

	int _tx_l1 = ibits * 2; // one for each input bit plus its index - worst case
	int _tx_l2 = svbits * 3;
	_tx_length = (_tx_l1 > _tx_l2? _tx_l1 : _tx_l2);

	_rx_buffer = (char *) malloc(_rx_length);
	_tx_buffer = (char *) malloc(_tx_length);
	
	Serial.begin(115200, SERIAL_8N2);
	timer.setInterval(250, pulse);
	
	pinMode(LED_BUILTIN, OUTPUT);

	inputValues = (int *) malloc(ibits * sizeof(int));

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
}

void loop() {
	timer.run();
}

void pulse() {
	inBd.retrieve();
}

void serialEvent() {
    while (Serial.available()) {
    	if (process_char(Serial.read()))
    		return;
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
		}
		break;

	case OUTPUT_OFF:
		if (_rx_index > 0) {
			int ox = (int) _rx_buffer[0];
			outBd.clearBit(ox);
			outBd.send();
		}
		break;
		
    case TURNOUT_NORMAL:
    case TURNOUT_REVERSE:
		if (_rx_index > 0) {
	    	int tx = (int) _rx_buffer[0];
	    	servo.setNR(tx, cmd == TURNOUT_NORMAL? 1 : 0);
		}
		break;

    case INPUT_DELTA:
    	inputDeltas();
    	break;
    	
    case INPUT_CURRENT:
    	inputCurrent();
    	break;
    	
    case IDENTIFY:
    	identify();
    	break;
    	
    case SERVO_ANGLE:
		if (_rx_index > 1) {
			int sv = (int) _rx_buffer[0];
			int angle = (int) _rx_buffer[1];
			
			servo.setValue(sv, angle);
		}
		break;

	case GET_TURNOUT:
		if (_rx_index > 0) {
			int tx = (int) _rx_buffer[0];
			int norm;
			int rev;
			int ini;

			servo.getLimits(tx, &norm, &rev);
			ini = servo.getInitialPosition(tx);
			_tx_buffer[0] = tx;
			_tx_buffer[1] = norm;
			_tx_buffer[2] = rev;
			_tx_buffer[3] = ini;
			_tx_index = 4;
			transmit(GET_TURNOUT);
		}
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
    	break;

	case STORE:
		storeLimits();
		break;
		
	default:
		return false;
	}
	
	acknowledge();
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
            else if (c == '0') {  //broadcast address
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
    Serial.write(255);
    Serial.write(255);
    Serial.write(STX);
    Serial.write(65 + _address);
    Serial.write(cmd);
    for (int i=0; i<_tx_index; i++)
    {
        if (_tx_buffer[i] == ETX)
            Serial.write(ESC); 
        if (_tx_buffer[i] == ESC)
            Serial.write(ESC); 
        Serial.write(_tx_buffer[i]);
    }
    Serial.write(ETX);
    Serial.flush();
}

#define SIGBYTE0 't'
#define SIGBYTE1 'c'
#define GENERATION 2

void loadLimits() {
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
	
	int nh = EEPROM.read(offset++);
	int nl = EEPROM.read(offset++);
	
	int nlimits = nh * 256 + nl;
	
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

void storeLimits() {
    int offset = 0;
    EEPROM.update(offset++, SIGBYTE0);
    EEPROM.update(offset++, SIGBYTE1);
    EEPROM.update(offset++, GENERATION);

    int n = servo.getNServos();
    EEPROM.update(offset++, n/256);
    EEPROM.update(offset++, n%256);
    _tx_index = 0;
    for (int i = 0; i<n; i++) {
		int norm, rev;
		if (servo.getLimits(i, &norm, &rev)) {
			if (_tx_index < _tx_length-2) {
				_tx_buffer[_tx_index++] = norm;
				_tx_buffer[_tx_index++] = rev;
			}

			EEPROM.update(offset++, norm/256);
			EEPROM.update(offset++, norm%256);
			EEPROM.update(offset++, rev/256);
			EEPROM.update(offset++, rev%256);
		}

		int pos = servo.getInitialPosition(i);
		if (pos >= 0) {
			if (_tx_index < _tx_length) {
				_tx_buffer[_tx_index++] = pos;
			}
			EEPROM.update(offset++, pos/256);
			EEPROM.update(offset++, pos%256);
		}
    }
    transmit(STORE);
}
