///////////////////////////////////////////////////////
//
// DCC Sniffer for Pacific Southern Railway - Low level
// logic credited to the following:
//     DCC packet analyze: Ruud Boer, October 2015
//     DCC packet capture: Robin McKay, March 2014
//
// The DCC signal is detected on Arduino digital pin 2
//
// Set the Serial Baud Rate to 115200
// ground pin 3 at start time to show all duplicates
// leave hi (default) to filter out duplicates
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

void getPacket() {
	preambleFound = false;
	packetEnd = false;
	packetBytesCount = 0;
	preambleOneCount = 0;
	while (! packetEnd) {
		if (preambleFound)
			getNextByte();
		else
			checkForPreamble();
	}
}

void checkForPreamble() {
	 byte nextBit = getBit();
	 if (nextBit == 1)
		preambleOneCount++;

	 if (preambleOneCount < 10 && nextBit == 0)
		preambleOneCount = 0;

	 if (preambleOneCount >= 10 && nextBit == 0)
		preambleFound = true;
}

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

byte getBit() {
	// gets the next bit from the bitBuffer
	// if the buffer is empty it will wait indefinitely for bits to arrive
	byte nbs = bitBuffHead;
	while (nbs == bitBuffHead)
		byte nbs = nextBitSlot(bitBuffTail); //Buffer empty

	bitBuffTail = nbs;
	return (bitBuffer[bitBuffTail]);
}

void beginBitDetection() {
	TCCR0A &= B11111100;
	attachInterrupt(0, startTimer, RISING);
}

void startTimer() {
	OCR0B = TCNT0 + DccBitTimerCount;
	TIMSK0 |= B00000100;
	TIFR0 |= B00000100;
}

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

byte nextBitSlot(byte slot) {
	slot ++;
	if (slot >= bitBufSize)
		slot = 0;
	return(slot);
}

//========================
//
// code beyond this point created by Jeff Bernardis for PSRY
//
//====================
char strBuf[32];
int dupPin = 3;
bool showDuplicates = false;

#define CMD_FOR    'f'
#define CMD_FOR128 'F'
#define CMD_REV    'r'
#define CMD_REV128 'R'
#define CMD_STOP   's'
#define CMD_ESTOP  'e'
#define CMD_F4F1   '1'
#define CMD_F8F5   '5'
#define CMD_F12F9  '9'

#define CMD_SPEED  'p' // these two are for internal use only
#define CMD_NULL   '0'

#define MAXPACKETS 64

int nPackets;
unsigned int locos[MAXPACKETS];
byte instrs[MAXPACKETS];
byte params[MAXPACKETS];

void packetListInit(void) {
	for (int i=0; i<MAXPACKETS; i++) {
		locos[i] = 0;
		instrs[i] = 0;
		params[i] = 0;
	}
	nPackets = 0;
}
		
bool addPacket(unsigned int loco, byte instr, byte param) {
	byte cmd;

	if (showDuplicates)
		return true;		

	if (instr == CMD_FOR || instr == CMD_FOR128 || instr == CMD_REV || instr == CMD_REV128 || instr == CMD_STOP || instr == CMD_ESTOP)
		cmd = CMD_SPEED;
	else
		cmd = instr;
			
	for (int i=0; i<nPackets; i++) {
		if (loco == locos[i] && cmd == instrs[i]) {
			if (param == params[i])
				// we've seem this loco before and parameter is still the same.  Filter it out
				return false;
				
			// we've seem this loco before but parameter has changed.  Show this message
			params[i] = param;
			return true;
		}
	}

	// otherwise - we've not seen this loco.  Record it and show the message
	int px = nPackets;
	if (nPackets+1 > MAXPACKETS) {
		for (int i=1; i<MAXPACKETS; i++) {
			locos[i-1] = locos[i];
			instrs[i-1] = instrs[i];
			params[i-1] = params[i];
		}
	}
	else
		nPackets++;
		
	locos[px] = loco;
	instrs[px] = cmd;
	params[px] = param;
	 
	return true;
}


void setup() {
	Serial.begin(115200);
	packetListInit();
	beginBitDetection(); 

	// check if we should see duplicates or not
	pinMode(dupPin, INPUT_PULLUP);
	showDuplicates = !digitalRead(dupPin);
}

void loop() {
	byte speed;
	byte checksum;
	byte cmd;
	byte param;
	bool decoderLoco;
	byte instruction;
	unsigned int decoderAddress;

	getPacket();
	
	pktByteCount = dccPacket[0];
	if (!pktByteCount)
		return; // No new packet available

	checksum = 0;
	for (byte n = 1; n <= pktByteCount; n++)
		checksum ^= dccPacket[n];
	
	if (checksum)
		return; // Invalid Checksum
	
	// There is a new packet with a correct checksum
	
	if (dccPacket[1]==B11111111)	//Idle packet
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

			byte speed = dccPacket[pktByteCount-1]&B01111111;
			if (!speed)
				cmd = CMD_STOP;
			else if (speed==1) {
				cmd = CMD_ESTOP;
				speed = 0;
			}
			else
				speed--;
			param = speed;
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
			
		param = speed;
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
			
		param = speed;
		break;

	case 4: // Loc Function L-4-3-2-1
		cmd = CMD_F4F1;
		param = instruction&B00011111;
		break;

	case 5: // Loc Function 8-7-6-5
		if (bitRead(instruction,4)) {
			cmd = CMD_F8F5;
			param = instruction&B00001111;
		}
		else { // Loc Function 12-11-10-9
			cmd = CMD_F12F9;
			param = instruction&B00001111;
		}
		break;

	}
	if (cmd != CMD_NULL) {		
		if (addPacket(decoderAddress, cmd, param)) {
			sprintf(strBuf, "%c %04d %3d", cmd, decoderAddress, param);
			Serial.println(strBuf);
		}
	}
}
