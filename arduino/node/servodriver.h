#ifndef SERVODRIVER_H
#define SERVODRIVER_H

#include <Adafruit_PWMServoDriver.h>

#define FIRSTADDR 0x40
#define MAX_SD_BOARDS 2
#define SERVOS_PER_BD 16

class ServoDriver {
	public:
		ServoDriver(void);
		void setup(int nservobds);
		void initialPositions();
		int getNServos(void);
		bool setLimits(int servo, int normal, int reverse);
		bool getLimits(int servo, int *normal, int *reverse);
		bool setInitialPosition(int servo, int pos);
		int getInitialPosition(int servo);
		bool setValue(int servo, int val);
		int getValue(int servo);
		bool getConfig(int tx, int *norm, int *rev,  int *ini, int *current);
		bool setNR(int servo, int NR);

	private:
		int nServos;
		int *lReverse;
		int *lNormal;
		int *lInitial;
		int *value;
		Adafruit_PWMServoDriver *pwm[MAX_SD_BOARDS];
};

#endif
