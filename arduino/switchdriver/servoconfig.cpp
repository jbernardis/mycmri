#include "servoconfig.h"


ServoConfig::ServoConfig(AT24C256 *eeprom) {
	_eeprom = eeprom;
	
	defaultNormal = 76;
	defaultReverse = 112;
	defaultSteps = 20;
}

void ServoConfig::loadConfig() {
	uint8_t tag[2];
	
	_eeprom -> read(0, (uint8_t *) tag, sizeof(tag));
	if (tag[0] != 0x48 || tag[1] != 0x49) {
		tag[0] = 0x48;
		tag[1] = 0x49;
		for (int i=0; i<2; i++)
			_eeprom -> write(i, (uint8_t *) tag+i, sizeof(uint8_t));

		for (int i=0; i<NSERVOS; i++) {
			last[i] = defaultNormal;
			normal[i] = defaultNormal;
			reverse[i] = defaultReverse;
			steps[i] = defaultSteps;
			writeOneServoConfig(i, defaultNormal, defaultNormal, defaultReverse, defaultSteps);
		}
	}
	else {
		for (int i=0; i<NSERVOS; i++) {
			last[i] = readOneServoConfig(i, LAST);
			normal[i] = readOneServoConfig(i, NORMAL);
			reverse[i] = readOneServoConfig(i, REVERSE);
			steps[i] = readOneServoConfig(i, STEPS);
		}
	}

}

int ServoConfig::calculateAddress(int sv, int dType) {
	int addr = -1;
	switch (dType) {
		case LAST:
			addr = TAGSIZE + sv * sizeof(short);
			break;

		case NORMAL:
			addr = TAGSIZE + BLOCKSIZE + sv * sizeof(short);
			break;

		case REVERSE:
			addr = TAGSIZE + BLOCKSIZE * 2 + sv * sizeof(short);
			break;

		case STEPS:
			addr = TAGSIZE + BLOCKSIZE * 3 + sv * sizeof(short);
			break;
	}
	return addr;
}

void ServoConfig::writeOneServoConfig(int sv, short vLast, short vNormal, short vReverse, short vSteps) {
		int addr = calculateAddress(sv, LAST);
		_eeprom -> write(addr, (uint8_t * ) &vLast, sizeof(short));
		
		addr = calculateAddress(sv, NORMAL);
		_eeprom -> write(addr, (uint8_t * ) &vNormal, sizeof(short));

		addr = calculateAddress(sv, REVERSE);
		_eeprom -> write(addr, (uint8_t * ) &vReverse, sizeof(short));

		addr = calculateAddress(sv, STEPS);
		_eeprom -> write(addr, (uint8_t * ) &vSteps, sizeof(short));	
}

short ServoConfig::readOneServoConfig(int sv, int dType) {
	int addr = calculateAddress(sv, dType);
	short value;
	_eeprom -> read(addr, (uint8_t *) &value, sizeof(short));
	return value;	
}

short ServoConfig::getValue(int sv, int dtype) {
	switch (dtype) {
		case LAST:
			return (last[sv]);
		case NORMAL:
			return (normal[sv]);
		case REVERSE:
			return (reverse[sv]);
		case STEPS:
			return (steps[sv]);
	}
	return (-1);
}
