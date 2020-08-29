#include "Arduino.h"

#include "outputboard.h"

#define BITS_PER_CHIP 8

void myShiftOut(int, int, byte);

OutputBoard::OutputBoard(int pinLatch, int pinClock, int pinData) {
	pLatch = pinLatch;
	pClock = pinClock;
	pData = pinData;
	nChips = 0;
}

void OutputBoard::setup(int chips) {
	pinMode(pLatch, OUTPUT);
	pinMode(pData, OUTPUT);  
	pinMode(pClock, OUTPUT);
	nChips = chips;
	for (int i = 0; i<MAX_OCHIPS; i++)
	    chipBits[i] = 0;

	send();
}

bool OutputBoard::setBit(int bit, bool val) {
	int cx = int(bit / BITS_PER_CHIP);
	int bx = bit % BITS_PER_CHIP;
	
	if (cx < 0 || cx >= nChips)
		return(false);
	if (bx < 0)
		return(false);

	if (val)
		chipBits[cx] = chipBits[cx] | (1 << bx);
	else
		chipBits[cx] = chipBits[cx] & ~(1 << bx);

	return (true);
}

bool OutputBoard::clearBit(int bit) {
	return (setBit(bit, false));
}

bool OutputBoard::toggleBit(int bit) {
	int cx = int(bit / BITS_PER_CHIP);
	int bx = bit % BITS_PER_CHIP;
	
	if (cx < 0 || cx >= nChips)
		return(false);
	if (bx < 0)
		return(false);

	int cv = chipBits[cx] & (1 << bx);
	if (cv != 0)
		return(setBit(bit, false));
	else
		return(setBit(bit, true));
}

int OutputBoard::getBit(int bit) {
	int cx = int(bit / BITS_PER_CHIP);
	int bx = bit % BITS_PER_CHIP;
	
	if (cx < 0 || cx >= nChips)
		return(-1);
	if (bx < 0)
		return(-1);

    int cv = chipBits[cx] & (1 << bx);
    if (cv != 0)
        return(1);
    else
        return(0);
}

void OutputBoard::send(void) {
	digitalWrite(pLatch, LOW);

	for (int i = nChips-1; i >= 0; i--)
		shiftByteOut(chipBits[i]);

	delay(50);

	digitalWrite(pLatch, HIGH);
}

void OutputBoard::shiftByteOut(byte d) {
	int pinState;
	digitalWrite(pData, LOW);
	digitalWrite(pClock, LOW);

	for (int i=7; i>=0; i--)  {
  		digitalWrite(pClock, LOW);

 		pinState = (d & (1<<i))? 1 : 0;

		digitalWrite(pData, (d & (1<<i))? 1 : 0);
		digitalWrite(pClock, HIGH);
		digitalWrite(pData, LOW);
	}
	digitalWrite(pClock, LOW);
}
