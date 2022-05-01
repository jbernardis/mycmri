///////////////////////////////////////////////////////
//
// DCC packet analyze: Ruud Boer, October 2015
// DCC packet capture: Robin McKay, March 2014
//
// The DCC signal is detected on Arduino digital pin 2
//
// Set the Serial Baud Rate to 115200
//
////////////////////////////////////////////////////////


#define TIMER_PRESCALER 64
#define DccBitTimerCount (F_CPU * 80L / TIMER_PRESCALER / 1000000L)
// 16000000 * 80 / 64 / 1000000 = 20; 20 x 4usecs = 80us

boolean packetEnd;
boolean preambleFound;

const byte bitBufSize = 50; // number of slots for bits
volatile byte bitBuffer[bitBufSize]; 
volatile byte bitBuffHead = 1;
volatile byte bitBuffTail = 0;

byte pktByteCount=0;
byte packetBytesCount;
byte preambleOneCount;
byte dccPacket[6]; // buffer to hold a packet

//========================

bool getPacket() {
  preambleFound = false;
  packetEnd = false;
  packetBytesCount = 0;
  preambleOneCount = 0;

  if (bitBuffHead == nextBitSlot(bitBuffTail))
  	return false;
  while (! packetEnd) {
    if (preambleFound)
      getNextByte();
    else
      checkForPreamble();
  }
  return true;
}

//========================

void checkForPreamble() {
   byte nextBit = getBit();
   if (nextBit == 1)
    preambleOneCount++;

   if (preambleOneCount < 10 && nextBit == 0)
    preambleOneCount = 0;

   if (preambleOneCount >= 10 && nextBit == 0)
    preambleFound = true;
}

//========================

void getNextByte() {
  byte newByte = 0;
  for (byte n = 0; n < 8; n++)
    newByte = (newByte << 1) + getBit();

  packetBytesCount ++;  
  dccPacket[packetBytesCount] = newByte;
  dccPacket[0] = packetBytesCount;
  if (getBit() == 1)
    packetEnd = true;
}

//========================

byte getBit() {
  // gets the next bit from the bitBuffer
  // if the buffer is empty it will wait indefinitely for bits to arrive
  byte nbs = bitBuffHead;
  while (nbs == bitBuffHead)
    byte nbs = nextBitSlot(bitBuffTail); //Buffer empty

  bitBuffTail = nbs;
  return (bitBuffer[bitBuffTail]);
}

//========================

void beginBitDetection() {
  TCCR0A &= B11111100;
  attachInterrupt(0, startTimer, RISING);
}

//========================

void startTimer() {
  OCR0B = TCNT0 + DccBitTimerCount;
  TIMSK0 |= B00000100;
  TIFR0 |= B00000100;
}

//========================

ISR(TIMER0_COMPB_vect) {
  byte bitFound = ! ((PIND & B00000100) >> 2); 
  TIMSK0 &= B11111011;
  byte nbs = nextBitSlot(bitBuffHead);
  if (nbs == bitBuffTail)
    return;
  else {
    bitBuffHead = nbs;
    bitBuffer[bitBuffHead] = bitFound;
  }
}

//========================

byte nextBitSlot(byte slot) {
  slot ++;
  if (slot >= bitBufSize)
    slot = 0;
  return(slot);
}

//========================

//====================

#include "locolist.h"

LocoList locoList;

char locoId[8];
int lx = 0;
char speedBuf[8];

unsigned long ledOff;

void setup() {
	Serial.begin(115200);
	beginBitDetection(); 
	pinMode(LED_BUILTIN, OUTPUT);
	digitalWrite(LED_BUILTIN, LOW);
	ledOff = 0;
}

void loop() {
	byte speed;
	byte checksum;
	byte cmd;
	bool decoderLoco;
	byte instruction;
	unsigned int decoderAddress;

	if (ledOff != 0) {
		if (millis() > ledOff) {
			digitalWrite(LED_BUILTIN, LOW);
			ledOff = 0;
		}
	}
	if (!getPacket()) 
		return; // No new packet available
	
	pktByteCount = dccPacket[0];
	if (!pktByteCount)
		return; // No new packet available

	checksum = 0;
	for (byte n = 1; n <= pktByteCount; n++)
		checksum ^= dccPacket[n];
	
	if (checksum)
		return; // Invalid Checksum
	
	// There is a new packet with a correct checksum
	
	if (dccPacket[1]==B11111111)  //Idle packet
		return;
	
	if (!bitRead(dccPacket[1],7)) { //bit7=0 -> Loc Decoder Short Address
		decoderAddress = dccPacket[1];
		instruction = dccPacket[2];
		decoderLoco = true;
	}
	else {
		if (bitRead(dccPacket[1],6)) { //bit7=1 AND bit6=1 -> Loc Decoder Long Address
			decoderAddress = 256 * (dccPacket[1] & B00111111) + dccPacket[2];
			instruction = dccPacket[3];
			decoderLoco = true;
		}
		else { //bit7=1 AND bit6=0 -> Accessory Decoder
			decoderAddress = dccPacket[1]&B00111111;
			instruction = dccPacket[2];
			decoderLoco = false;
		}
	}
	if (!decoderLoco) 
		return;

	byte instructionType = instruction>>5;
	cmd = CMD_NULL;

	switch (instructionType) {
	case 1: // Advanced Operations
		if (instruction==B00111111) { //128 speed steps
			if (bitRead(dccPacket[pktByteCount-1],7))
				cmd = CMD_FOR128;
			else
				cmd = CMD_REV128;
			
			speed = dccPacket[pktByteCount-1]&B01111111;
			if (!speed)
				cmd = CMD_STOP;
			else if (speed==1) {
				cmd = CMD_ESTOP;
			speed = 0;
		}
		else
			speed--;
		}
		break;

	case 2: // Reverse speed step
		speed = ((instruction&B00001111)<<1) - 3 + bitRead(instruction,4);
		if (speed==253 || speed==254) {
			cmd = CMD_STOP;
			speed = 0;
		}
		else if (speed==255 || speed==0) {
			cmd = CMD_ESTOP;
			speed = 0;
		}
		else 
			cmd = CMD_REV;
		break;

	case 3: // Forward speed step
		speed = ((instruction&B00001111)<<1) - 3 + bitRead(instruction,4);
		if (speed==253 || speed==254) {
			cmd = CMD_STOP;
			speed = 0;
		}
		else if (speed==255 || speed==0) {
			cmd = CMD_ESTOP;
			speed = 0;
		}
		else 
			cmd = CMD_FOR;
		break;
	}
	if (cmd != CMD_NULL) {    
		if (locoList.addLoco(decoderAddress, cmd, speed)) {
			digitalWrite(LED_BUILTIN, HIGH);
			ledOff = millis() + 200;
		}
	}
}

void serialEvent() {
    char c = Serial.read();
    if (c == '\n') {
		int lid = atoi(locoId);
		Serial.println(locoList.getLocoSpeed(lid));
		lx = 0;
    }
    else {
    	if (isDigit(c)) {
			locoId[lx++] = c;
			locoId[lx] = '\0';
    	}
	}
}
