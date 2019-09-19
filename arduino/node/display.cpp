#include <stdio.h>
#include <cstring>
#include "display.h"


need an include and declaration for the lcd

Display::Display(int a, int nin, int nout, int nsrv) {
	addr = a;
	nInputBits = nin;
	nInputBytes = (nin%8 == 0) ? nin/8 : nin/8+1;
	nOutputBits = nout;
	nOutputBytes = (nout%8 == 0) ? nout/8 : nout/8+1;
	nServoBits = nsrv;
	nServoBytes = (nsrv%8 == 0) ? nsrv/8 : nsrv/8+1;
	enabled = true;
}

void Display::setup(bool state) {
	lcd.begin(20, 4);
	enable(state);
}

void Display::enable(bool f) {
	enabled = f;
	lcd.setBacklight(enabled? HIGH : LOW);
	lcd.clear();
	if (enabled)
		lcd.display();
	else
		lcd.noDisplay();
}

void Display::clear(void) {
	if (!enabled)
		return;
	lcd.clear();
}

void Display::showAddress(void) {
	char buffer[21];
	if (!enabled)
		return;
	lcd.setCursor(0, 0);
	sprintf(buffer, "A:%2d I:%2d O:%2d S:%2d", addr, nInputBits, nOutputBits, nServoBits);
	lcd.print(buffer);
}

void Display::showInput(int *d) {
	showData("I", 1, d, nInputBytes);
}

void Display::showOutput(int *d) {
	showData("O", 2, d, nOutputBytes);
}

void Display::showServos(int *d) {
	showData("S", 3, d, nServoBytes);
}

void Display::showData(const char *label, int line, int* data, int byteCount) {
	char buffer[21];
	char buf2[4];
	if (!enabled)
		return;
	lcd.setCursor(0, line);
	sprintf(buffer, "%s:", label);
	for (int i=0; i<byteCount; i++) {
		sprintf(buf2, " %02x", *(data+i));
		strcat(buffer, buf2);
	}
	lcd.print(buffer);
}

