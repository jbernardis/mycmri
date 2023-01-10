#include "Arduino.h"
#include "Wire.h"
#include "at24c256.h"

AT24C256::AT24C256(int address) {
	Wire.begin();
	_address = address;
}

void AT24C256::write(uint16_t writeAddress, uint8_t* data, uint8_t len) {
	Wire.beginTransmission(_address);
	Wire.write((byte)(writeAddress & 0xFF00) >> 8);
	Wire.write((byte)(writeAddress & 0x00FF));

	for (int i=0; i<len; i++) {
		Wire.write(data[i]);
		delay(5);
	}
	Wire.endTransmission();
}

void AT24C256::read(uint16_t readAddress, uint8_t* data, uint8_t len) {
	Wire.beginTransmission(_address);
	Wire.write((byte)(readAddress & 0xFF00) >> 8);
	Wire.write((byte)(readAddress & 0x00FF));
	Wire.endTransmission();

	Wire.requestFrom(_address, (int) len);
	for (int i=0; i<len; i++){
		if(Wire.available()) {
			data[i] = Wire.read();
			delay(5);
		}
	}
}
