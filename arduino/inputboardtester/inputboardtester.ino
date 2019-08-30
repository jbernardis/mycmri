
#include "InputBoard.h"

#define CHIPS 2

// InputBoard::InputBoard(int pinLatch, int pinClock, int pinClockEnable, int pinData, int chips) 
// InputBoard::InputBoard(int pinLatch, int pinClock, int pinClockEnable, int pinData) - chips = 2
InputBoard inBd(8, 9, 11, 12, CHIPS);

unsigned long pinValues;

void setup() {
    Serial.begin(9600);
    inBd.setup();
}

void loop() {
    inBd.retrieve();
    for (int i=0; i<CHIPS * BITS_PER_CHIP; i++) {
        Serial.print(i);
        Serial.print(": ");
        Serial.println(inBd.getBit(i));
    }

    for (int i=0; i<CHIPS; i++) {
    	Serial.print("CHIP ");
    	Serial.print(i);
    	Serial.print(": ");
    	for (int j=0; j<BITS_PER_CHIP; j++) {
    		Serial.print(inBd.getChipBit(i, j));
    	}
    	Serial.println("");
    }
    delay(5000);
}
