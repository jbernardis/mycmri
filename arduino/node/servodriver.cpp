#include "servodriver.h"

int defaultNormal = 76;
int defaultReverse = 112;

ServoDriver::ServoDriver(void) {
	nServos = 0;
}

void ServoDriver::setup(int nservobds) {
	nServos = nservobds * SERVOS_PER_BD;
	
	lReverse = (int *) malloc(nServos * sizeof(int));
	lNormal = (int *) malloc(nServos * sizeof(int));
	lInitial = (int *) malloc(nServos * sizeof(int));
	value = (int *) malloc(nServos * sizeof(int));
  
	for (int i=0; i<nservobds; i++) {
		pwm[i] = new Adafruit_PWMServoDriver(FIRSTADDR+i);
		pwm[i]->begin();
		pwm[i]->setOscillatorFrequency(27000000);
		pwm[i]->setPWMFreq(50);
	}
		
	for (int i=0; i<nServos; i++) {
		*(lNormal+i) = defaultNormal;
		*(lReverse+i) = defaultReverse;
		*(lInitial+i) = defaultNormal;
	}
}

void ServoDriver::initialPositions() {			
	for (int i=0; i<nServos; i++) {
		delay(50);
		setValue(i, *(lInitial+i)); 
	}
}

int ServoDriver::getNServos() {
	return nServos;
}

bool ServoDriver::setLimits(int servo, int normal, int reverse) {
	if (servo < 0 || servo >= nServos)
		return(false);
	
	*(lNormal+servo) = normal;
	*(lReverse+servo) = reverse;
	return(true);
}

bool ServoDriver::setInitialPosition(int servo, int pos) {
	if (servo < 0 || servo >= nServos)
		return(false);
	
	*(lInitial+servo) = pos;
	return(true);
}

bool ServoDriver::getLimits(int servo, int *normal, int *reverse) {
	if (servo < 0 || servo >= nServos)
		return(false);
	
	*normal = *(lNormal+servo);
	*reverse = *(lReverse+servo);
	return(true);
}

int ServoDriver::getInitialPosition(int servo) {
	if (servo < 0 || servo >= nServos)
		return(-1);
	
	return(*(lInitial+servo));
}

bool ServoDriver::setValue(int servo, int val) {
	if (servo < 0 || servo >= nServos)
		return(false);

	if (val == *(value+servo))
		return(true);

	*(value+servo) = val;
	int dx = servo/SERVOS_PER_BD;
	int sx = servo%SERVOS_PER_BD;

	int sv = map(val, 0, 180, 150, 600);

	pwm[dx]->setPWM(sx, 0, sv);
	return(true);
}

int ServoDriver::getValue(int servo) {
	if (servo < 0 || servo >= nServos)
		return(0);

	return (*(value+servo));
}

bool ServoDriver::setNR(int servo, int NR) {
	if (servo < 0 || servo >= nServos)
		return(false);

	if (NR == 1)
		return(setValue(servo, *(lNormal+servo)));
	else
		return(setValue(servo, *(lReverse+servo)));
}
