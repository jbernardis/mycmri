#include "servodriver.h"

const int defaultReverse = 0;
const int defaultNormal = 180;

ServoDriver::ServoDriver(int nservobds) {
    if (nservobds > MAX_SD_BOARDS) {
        nServoBds = MAX_SD_BOARDS;
        nServos = MAX_SD_BOARDS * SERVOS_PER_BD;
    }
    else {
        nServos = nservobds * SERVOS_PER_BD;
        nServoBds = nservobds;
    }
        
	lReverse = (int *) malloc(nServos * sizeof(int));
	lNormal = (int *) malloc(nServos * sizeof(int));
	value = (int *) malloc(nServos * sizeof(int));
}

void ServoDriver::setup() {
	for (int i=0; i<nServoBds; i++) {
		pwm[i] = new Adafruit_PWMServoDriver(FIRSTADDR+i);
		pwm[i]->begin();
		pwm[i]->setPWMFreq(60);
	}
		
	for (int i=0; i<nServos; i++) {
		*(lNormal+i) = defaultNormal;
		*(lReverse+i) = defaultReverse;
		*(value+i) = -1;
	}
}

bool ServoDriver::setLimits(int servo, int normal, int reverse) {
	if (servo < 0 || servo >= nServos)
		return(false);

	*(lNormal+servo) = normal;
	*(lReverse+servo) = reverse;
	return(true);
}

bool ServoDriver::setValue(int servo, int val) {
	if (servo < 0 || servo >= nServos)
		return(false);

	if (val == (value+servo))
		return(true);

	*(value+servo) = val;
	int dx = servo/SERVOS_PER_BD;
	int sx = servo%SERVOS_PER_BD;
	pwm[dx]->setPWM(sx, 0, val);
	return(true);
}

bool ServoDriver::setNormal(int servo) {
	if (servo < 0 || servo >= nServos)
		return(false);

	return(setValue(servo, *(lNormal+servo)));
}

bool ServoDriver::setReverse(int servo) {
	if (servo < 0 || servo >= nServos)
		return(false);

	return(setValue(servo, *(lReverse+servo)));
}
