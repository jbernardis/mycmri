#include <stdio.h>

#include "input.h"

Input::Input(void) {
	for (int i=0; i<NIBITS; i++) {
		currentState[i] = true;
	}
}

void Input::setState(int ix, bool newState) {
	if (ix < 0 || ix >= NIBITS) {
		printf("ignoring request to set input state because index is out of range\n");
		return;
	}

	currentState[ix] = newState;
}

bool Input::getState(int ix) {
	if (ix < 0 || ix >= NIBITS) {
		printf("request to get input state: index is out of range\n");
		return true;
	}

	return currentState[ix];
}
