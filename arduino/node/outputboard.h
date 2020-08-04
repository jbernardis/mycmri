#ifndef OUTPUTBOARD_H
#define OUTPUTBOARD_H

#define MAX_OCHIPS 8

class OutputBoard {
	public:
		OutputBoard(int pinLatch, int pinClock, int pinData);
		void setup(int nChips);
		bool setBit(int bit, bool val=true);
		bool clearBit(int bit);
		bool toggleBit(int bit);
		bool getBit(int bit);
		void send(void);

	private:
		int nChips, pLatch, pClock, pData;
		int chipBits[MAX_OCHIPS];
		void shiftByteOut(byte);
};

#endif
