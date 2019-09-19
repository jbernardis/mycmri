#include <Adafruit_PWMServoDriver.h>
#include <Auto485.h>
#include <CMRI.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>

#include "inputboard.h"
#include "outputboard.h"
#include "servodriver.h"

#define CMRI_ADDR 0
#define ICHIPS 2
#define OCHIPS 2
#define SERVOBDS 1

const int ibits = ICHIPS * 8;
const int obbits = OCHIPS * 8;
const int svbits = SERVOBDS * 16;
const int obits = obbits + svbits;

// Instantiate the rs485 bus and CMRI interface
Auto485 bus(2);
CMRI cmri(CMRI_ADDR, ibits, obits, bus);

// Instantiate the object for  Input Boards
// InputBoard::InputBoard(int pinLatch, int pinClock, int pinClockEnable, int pinData, int circuits) 
InputBoard inBd(8, 9, 11, 12, ICHIPS);

// Instantiate the object for output boards
OutputBoard outBd(3, 4, 5, OCHIPS);

// Instantiate the servo driver
ServoDriver svDrv(SERVOBDS);

// Instantiate the LCD display 
hd44780_I2Cexp lcd(0x20);

char tmp[10];
void setup() {
    lcd.begin(20, 4);
    lcd.print("hello, world!");
    lcd.setBacklight(HIGH);
    
    inBd.setup();
    outBd.setup();
    svDrv.setup();
    
    // start the RS485 bus
    bus.begin(19200, SERIAL_8N2);
}

void loop() {
	// retrieve inputs and put them in the CMRI object
	inBd.retrieve();
	for (int i=0; i<ibits; i++) {
        Serial.print(i);
        Serial.print(": ");
        cmri.set_bit(i, inBd.getBit(i));
    }

	// send inputs to host and retrieve the latest outputs from host
	cmri.process();

	// send the outputs to the actual output channels
	for (int i=0; i<obbits; i++) {
		outBd.setBit(i, cmri.get_bit(i));		
	}

	// servos are offset after the normal output channels
    // true -> set to normal position, false -> reverse
	for (int i=0; i<svbits; i++) {
		if (cmri.get_bit(i+obbits))
            svDrv.setNormal(i);
        else
            svDrv.setReverse(i);
	}
}
