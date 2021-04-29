#include <stdio.h>

#include "output.h"

Output::Output(void) {
	for (int i=0; i<NOBITS; i++) {
		currentValue[i] = 0;
	}
}

void Output::setValue(int ix, int newValue) {
	if (ix < 0 || ix >= NOBITS) {
		printf("ignoring request to set output value because index is out of range\n");
		return;
	}

	currentValue[ix] = newValue;
}

int Output::getValue(int ix) {
	if (ix < 0 || ix >= NOBITS) {
		printf("request to get output value: index is out of range\n");
		return 0;
	}

	return currentValue[ix];
}
