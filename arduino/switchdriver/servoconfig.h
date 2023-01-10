#ifndef SERVOCONFIG_H
#define SERVOCONFIG_H

#include "at24c256.h"

#define NSERVOS 16

#define LAST 0
#define NORMAL 1
#define REVERSE 2
#define STEPS 3

#define TAGSIZE 2
#define BLOCKSIZE (NSERVOS * sizeof(short))

class ServoConfig {
	public:
		ServoConfig(AT24C256 *);
		void loadConfig(void);
		short getValue(int, int);

	private:
		AT24C256 * _eeprom;
		void writeOneServoConfig(int, short, short, short, short);
		short readOneServoConfig(int, int);
		int calculateAddress(int, int);
		
		short defaultNormal;
		short normal[NSERVOS];

		short defaultReverse;
		short reverse[NSERVOS];
		
		short last[NSERVOS];

		short defaultSteps;
		short steps[NSERVOS];
};


#endif
