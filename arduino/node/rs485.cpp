#include "rs485.h"

RS485::RS485(int dePin) {
	_dePin = dePin;
	_mode = RX;
	pinMode(_dePin, OUTPUT);
}

void RS485::setMode(char mode) {
	if (_mode == TX && mode == RX)
		Serial.flush();

	if (mode != _mode) {
		_mode = mode;
		digitalWrite(_dePin, _mode == TX);
	}
}

void RS485::begin(unsigned long baud) {
	Serial.begin(baud);
}

void RS485::begin(unsigned long baud, uint8_t config) {
	Serial.begin(baud, config);
}

void RS485::end(void) {
	Serial.end();
}

int RS485::available(void) {
	return(Serial.available());
}

int RS485::read(void) {
	if (_mode != RX)
		setMode(RX);
	return (Serial.read());
}

size_t RS485::write(uint8_t c) {
	if (_mode != TX)
		setMode(TX);
	return (Serial.write(c));
}

void RS485::flush(void) {
	Serial.flush();
	setMode(RX);
}
