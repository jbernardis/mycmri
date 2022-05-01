#include <Arduino.h>
#include "locolist.h"

LocoList::LocoList(void) {
	for (int i=0; i<MAXLOCOS; i++) {
		locos[i] = 0;
		cmds[i] = 0;
		speeds[i] = 0;
	}
	nLocos = 0;
	nextSlot = 0;
}


bool LocoList::addLoco(unsigned int loco, byte cmd, byte speed) {
	for (int i=0; i<nLocos; i++) {
		if (loco == locos[i]) {
			if (speed == speeds[i] && cmd == cmds[i]) {
				return false;
			}
	
			speeds[i] = speed;
			cmds[i] = cmd;
			return true;
		}
	}

	int px = nextSlot;
	if (nLocos < MAXLOCOS) {
		// still room in the original array
		px = nLocos++;
	}
	else {
		// just over-write the earlier entries in the array
		nextSlot++;
		if (nextSlot >= MAXLOCOS)
			nextSlot = 0;
	}

	locos[px] = loco;
	cmds[px] = cmd;
	speeds[px] = speed;
	
	return true;
}

char * LocoList::getLocoSpeed(int loco) {
	for (int i=0; i<nLocos; i++) {
		if (loco == locos[i]) {
			sprintf(speedString, "%3d %c", speeds[i], cmds[i]);
			return speedString;
		}
	}
	strcpy(speedString, "??? ?");
	return speedString;
}
