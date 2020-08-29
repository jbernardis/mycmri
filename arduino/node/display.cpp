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

void Display::update(void) {
	if (clearTimer <= 0)
		return;

	clearTimer--;
	if (clearTimer == 0) {
		clear();
	}
}

void Display::clear(void) {
	lcd.clear();
	lcd.setBacklight(0);
}

void Display::setBacklight(bool flag) {
	if (flag) 
		lcd.setBacklight(255);
	else
		lcd.setBacklight(0);
}

void Display::showConfig(void) {
	lcd.setCursor(0, 0);
	sprintf(buffer, "A:%2d", addr);
	lcd.print(buffer);
	
	lcd.setCursor(0, 1);
	sprintf(buffer, "I:%2d / O:%2d / S:%2d", nInputBytes, nOutputBytes, nServoDrivers);
	lcd.print(buffer);

	lcd.setBacklight(255);
	clearTimer = 30;
}

void Display::outputOn(int ox) {
	sprintf(buffer, "Output ON: %2d     ", ox);
	displayAndTime();
}

void Display::outputOff(int ox) {
	sprintf(buffer, "Output OFF: %2d    ", ox);
	displayAndTime();
}

void Display::turnoutNormal(int tx) {
	sprintf(buffer, "TO Normal: %2d     ", tx);
	displayAndTime();
}

void Display::turnoutReverse(int tx) {
	sprintf(buffer, "TO Reverse: %2d    ", tx);
	displayAndTime();
}
	
void Display::servoAngle(int sx, int angle){
	sprintf(buffer, "Servo %2d angle %2d ", sx, angle);
	displayAndTime();
}

void Display::message(const char * msg) {
	strcpy(buffer, msg);
	displayAndTime();
}

void Display::displayAndTime(void) {
	lcd.setCursor(0, 3);
	lcd.print(buffer);

	if (clearTimer < 10) 
		clearTimer = 10;	
}
