#include <SimpleTimer.h>
#include "inputboard.h"
#include "servodriver.h"
#include "servoconfig.h"
#include "at24c256.h"

AT24C256 eeprom(0x50);

#define SP_NORMAL 1
#define SP_REVERSE 0

SimpleTimer timer;

InputBoard inBd(8, 9, 6, 7);
int ibits = 32;
int ichips = 4;
int * inputValues;

ServoDriver servo;
ServoConfig svcfg(&eeprom);

void setup() {
	Serial.begin(9600);
	inputValues = (int *) malloc(ibits * sizeof(int));
	inBd.setup(ichips);

	inBd.retrieve();
	for (int i=0; i<ibits; i++) {
		*(inputValues+i) = inBd.getBit(i);
	}

	servo.setup(1, 0x41);
	svcfg.loadConfig();
	
	for (int i=0; i<NSERVOS; i++) {
		servo.setLimits(i, svcfg.getValue(i, NORMAL), svcfg.getValue(i, REVERSE));
		servo.setSteps(i, svcfg.getValue(i, STEPS));
		servo.setInitialPosition(i, svcfg.getValue(i, STEPS));
	}

	servo.initialPositions();

	timer.setInterval(100, pulse);
}

void loop() {
	timer.run();
}

void pulse() {
	servo.update();
	inBd.retrieve();
	for (int i=0; i<ibits; i++) {
		int bv = inBd.getBit(i);
		if (bv != *(inputValues+i)) {
			*(inputValues+i) = bv;
			if (bv == 0) {
				int sv = i/2;
				int direction = i%2 == 0? SP_NORMAL : SP_REVERSE;
				int nv = servo.setNR(sv, direction);
				Serial.print("new target value = ");
				Serial.println(nv);
			}
		}
	}
}
