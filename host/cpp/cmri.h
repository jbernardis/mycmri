#ifndef CMRI_H
#define CMRI_H

#include "rs485bus.h"

class CMRI {
	public:
		CMRI(int, RS485Bus *, void (*)(int, int, int), int inbytes=3, int outbytes=6);
		void process(void);
		bool setOutputBit(int, int);
		bool outputPending(void);
		void transmit(void);
		void poll(void);

	private:
		void (*inputChange)(int, int, int);
		char nodeAddr;
		int numericAddr;
		RS485Bus *rs485Bus;
		int inBytes;
		int outBytes;
		char *inBuffer;
		char *newInBuffer;
		char *outBuffer;
		char *lastOutBuffer;
};

#endif
