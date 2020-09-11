#include <stdio.h>
#include "display.h"
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27); // set the LCD address to 0x27

Display::Display(void) {
	clearTimer = 0;
}

void Display::nodeConfig(int a, int nin, int nout, int nsrv) {
	addr = a;
	nInputBytes = nin;
	nOutputBytes = nout;
	nServoDrivers = nsrv;
}

void Display::begin(void) {
	lcd.begin(20, 4);
    lcd.setBacklight(255);
    lcd.noBlink();
    lcd.noCursor();
    clearTimer = 0;
}

bool Display::update(void) {
	if (clearTimer <= 0)
		return false;

	clearTimer--;
	if (clearTimer == 0) {
		clear();
		return true;
	}
	return false;
}

void Display::clear(void) {
	lcd.clear();
}

void Display::showConfig(void) {
	sprintf(buffer, "A:%2d", addr);
	displayOnLine(buffer, 0, 10);
	
	sprintf(buffer, "I:%2d / O:%2d / S:%2d", nInputBytes, nOutputBytes, nServoDrivers);
	displayOnLine(buffer, 1, 10);
}

void Display::outputOn(int ox) {
	sprintf(buffer, "Output ON: %2d", ox);
	displayOnLine(buffer, 3, 10);
}

void Display::outputOff(int ox) {
	sprintf(buffer, "Output OFF: %2d    ", ox);
	displayOnLine(buffer, 3, 10);
}

void Display::turnoutNormal(int tx) {
	sprintf(buffer, "TO Normal: %2d     ", tx);
	displayOnLine(buffer, 3, 10);
}

void Display::turnoutReverse(int tx) {
	sprintf(buffer, "TO Reverse: %2d    ", tx);
	displayOnLine(buffer, 3, 10);
}
	
void Display::servoAngle(int sx, int angle){
	sprintf(buffer, "Servo %2d angle %2d ", sx, angle);
	displayOnLine(buffer, 3, 10);
}

void Display::message(const char * msg) {
	if (strlen(msg) > 20) {
		strncpy(buffer, msg, 20);
		buffer[20] = '\0';
	}
	else {
		strcpy(buffer, msg);
	}
	displayOnLine(msg, 3, 10);
}

void Display::showInputChip(int cx, int cv) {
	sprintf(buffer, "ICHIP %d: %02x", cx, cv);
	displayOnLine(buffer, 0, 10);
	displayOnLine("", 1, 10);
}

void Display::showOutputChip(int cx, int cv) {
	sprintf(buffer, "OCHIP %d: %02x", cx, cv);
	displayOnLine(buffer, 0, 10);
	displayOnLine("", 1, 10);
}

void Display::showServo(int sx, int norm, int rev, int ini, int curr) {
	sprintf(buffer, "SV %d: n/r/i/c", sx);
	displayOnLine(buffer, 0, 10);
	sprintf(buffer, "%d/%d/%d/%d", norm, rev, ini, curr);
	displayOnLine(buffer, 1, 10);
}

void Display::displayOnLine(char *s, int l, int t) {
	sprintf(dbuf, "%-20s", s);
	lcd.setCursor(0, l);
	lcd.print(dbuf);
	clearTimer = t;
}
