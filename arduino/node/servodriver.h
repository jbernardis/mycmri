#ifndef SERVODRIVER_H
#define SERVODRIVER_H

#define FIRSTADDR 0x40
#include <Adafruit_PWMServoDriver.h>
#define MAX_SD_BOARDS 2
#define SERVOS_PER_BD 16

class ServoDriver {
	public:
		ServoDriver(int nservos);
		void setup(void);
		bool setLimits(int servo, int normal, int reverse);
		bool setValue(int servo, int val);
		bool setNormal(int servo);
		bool setReverse(int servo);

	private:
		int nServos;
        int nServoBds;
		int *lReverse;
		int *lNormal;
		int *value;
		Adafruit_PWMServoDriver *pwm[MAX_SD_BOARDS];
};

#endif
