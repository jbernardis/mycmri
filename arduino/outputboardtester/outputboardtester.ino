#include "outputboard.h"

#define NCHIPS 2

OutputBoard ob(3,4,5,NCHIPS);

int bx = 0;

void setup() {
	Serial.begin(9600);
	ob.setup();
	for (int i = 0; i<NCHIPS*OBITS_PER_CHIP; i++)
		ob.clearBit(i);
}

void loop() {
	Serial.print("bit ");
	Serial.println(bx);

	ob.setBit(bx);
	ob.setBit(bx+8);
	ob.send();
	delay(1000);
	ob.clearBit(bx);
	ob.clearBit(bx+8);
	bx++;
	ob.send();
	delay(100);
	if (bx >= OBITS_PER_CHIP)
		bx = 0;
}
