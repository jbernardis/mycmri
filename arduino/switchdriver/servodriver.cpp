#include "servodriver.h"

int defaultNormal = 76;
int defaultReverse = 112;
int defaultSteps = 20;

ServoDriver::ServoDriver(void) {
	nServos = 0;
}

void ServoDriver::setup(int nservobds) {
	setup(nservobds, FIRSTADDR);
}

void ServoDriver::setup(int nservobds, int firstaddr) {
	nServos = nservobds * SERVOS_PER_BD;

	lReverse = (int *) malloc(nServos * sizeof(int));	
	lNormal = (int *) malloc(nServos * sizeof(int));
	lInitial = (int *) malloc(nServos * sizeof(int));
	lSteps = (int *) malloc(nServos * sizeof(int));
	
	value = (int *) malloc(nServos * sizeof(int));
	start = (int *) malloc(nServos * sizeof(int));
	target = (int *) malloc(nServos * sizeof(int));
	stepcount = (int *) malloc(nServos * sizeof(int));
	stepsize = (float *) malloc(nServos * sizeof(float));
  
	for (int i=0; i<nservobds; i++) {
		pwm[i] = new Adafruit_PWMServoDriver(firstaddr+i);
		pwm[i]->begin();
		pwm[i]->setOscillatorFrequency(27000000);
		pwm[i]->setPWMFreq(50);
	}
		
	for (int i=0; i<nServos; i++) {
		*(lNormal+i) = defaultNormal;
		*(lReverse+i) = defaultReverse;
		*(lInitial+i) = defaultNormal;
		*(lSteps+i) = defaultSteps;
		*(target+i) = 0;
		*(value+i) = 0;
	}
}

void ServoDriver::initialPositions() {			
	for (int i=0; i<nServos; i++) {
		setPWM(i, *(lInitial+i)); 
		*(target+i) = *(lInitial+i);
		*(value+i) = *(lInitial+i);
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

bool ServoDriver::setSteps(int servo, int nsteps) {
	if (servo < 0 || servo >= nServos)
		return(false);
	
	*(lSteps+servo) = nsteps;
	Serial.print("set servo ");
	Serial.print(servo);
	Serial.print(" steps to ");
	Serial.print(*(lSteps+servo));
	Serial.print(" ");
	Serial.println(nsteps);
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

int ServoDriver::getSteps(int servo) {
	if (servo < 0 || servo >= nServos)
		return(-1);
	
	return(*(lSteps+servo));
}

bool ServoDriver::getConfig(int servo, int *normal, int *reverse, int *initial, int *current, int *nsteps) {
	if (servo < 0 || servo >= nServos)
		return(false);
	
	*normal = *(lNormal+servo);
	*reverse = *(lReverse+servo);
	*initial = *(lInitial+servo);
	*current = *(value+servo);
	*nsteps = *(lSteps+servo);
	return(true);
}


int ServoDriver::setValue(int servo, int val) {
	return (setValue(servo, val, *(lSteps+servo)));
}

int ServoDriver::setValue(int servo, int val, int nsteps) {
	Serial.print("set servo ");
	Serial.print(servo);
	Serial.print(" to ");
	Serial.print(val);
	Serial.print(" in ");
	Serial.print(nsteps);
	Serial.println(" steps");
	if (servo < 0 || servo >= nServos)
		return(-1);

	if (val == *(value+servo))
		return(-1);

	*(target+servo) = val;
	*(start+servo) = *(value+servo);
	*(stepcount+servo) = 0;

	float szstep = (float) (abs(*(lReverse+servo)-*(lNormal+servo))) / nsteps;
	if (*(value+servo) < *(target+servo)) {
		*(stepsize+servo) = szstep;
		if (*(stepsize+servo) < 1)
			*(stepsize+servo) = 1;
	}
	else if (*(value+servo) > *(target+servo)) {
		*(stepsize+servo) = - szstep;
		if (*(stepsize+servo) > -1)
			*(stepsize+servo) = -1;
	}
	
	return(val);
}

void ServoDriver::update(void) {
	for (int i=0; i<nServos; i++) {
		if (*(value+i) != *(target+i)) {
			*(stepcount+i) = *(stepcount+i) + 1;
			*(value+i) = *(start+i) + (int) (*(stepcount+i) * *(stepsize+i));
			if (*(stepsize+i) < 0 && *(value+i) < *(target+i))
				*(value+i) = *(target+i);
			else if (*(stepsize+i) > 0 && *(value+i) > *(target+i))
				*(value+i) = *(target+i);
				
			setPWM(i,*(value+i));
			
		}
	}
}

void ServoDriver::setPWM(int servo, int value) {
		int dx = servo/SERVOS_PER_BD;
		int sx = servo%SERVOS_PER_BD;

		int sv = map(value, 0, 180, 150, 600);

		pwm[dx]->setPWM(sx, 0, sv);	
}

int ServoDriver::getValue(int servo) {
	if (servo < 0 || servo >= nServos)
		return(0);

	return (*(value+servo));
}

int ServoDriver::setNR(int servo, int NR) {
	if (servo < 0 || servo >= nServos)
		return(false);

	if (NR == 1)
		return(setValue(servo, *(lNormal+servo)));
	else
		return(setValue(servo, *(lReverse+servo)));
}
