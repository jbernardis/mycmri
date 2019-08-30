#include <Auto485.h>
#include <CMRI.h>

#define CMRI_ADDR 0
#define DE_PIN 2

Auto485 bus(DE_PIN);
CMRI cmri(CMRI_ADDR, 24, 48, bus);

#include <Wire.h>
#include <LiquidTWI2.h>

LiquidTWI2 lcd(0x20);

char tmp[10];

void setup() {
    lcd.setMCPType(LTI_TYPE_MCP23008); 
    lcd.begin(20, 4);
    lcd.print("hello, world!");
    lcd.setBacklight(HIGH);

    bus.begin(19200, SERIAL_8N2);
}

void loop() {
	cmri.process();
	for (int i=0; i<6; i++) {
		char b = cmri.get_byte(i);
		lcd.setCursor(i*3, 1);
		sprintf(tmp, "%02x", (int(b) & 0xff));
		lcd.print(tmp);
	}
}
