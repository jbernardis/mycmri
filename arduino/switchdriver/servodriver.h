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
		void setup(int nservobds, int firstaddr);
		void initialPositions();
		int getNServos(void);
		bool setLimits(int servo, int normal, int reverse);
		bool getLimits(int servo, int *normal, int *reverse);
		bool setInitialPosition(int servo, int pos);
		bool setSteps(int servo, int nsteps);
		int getInitialPosition(int servo);
		int getSteps(int servo);
		int setValue(int servo, int val);
		int setValue(int servo, int val, int nsteps);
		int getValue(int servo);
		bool getConfig(int tx, int *norm, int *rev,  int *ini, int *current, int *nsteps);
		int setNR(int servo, int NR);
		void setPWM(int servo, int value);
		void update(void);

	private:
		int nServos;
		int *lReverse;
		int *lNormal;
		int *lInitial;
		int *lSteps;
		int *value;
		int *start;
		int *target;
		int *stepcount;
		float *stepsize;
		int steps;
		Adafruit_PWMServoDriver *pwm[MAX_SD_BOARDS];
};

#endif
