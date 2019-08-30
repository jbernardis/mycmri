#define INIT  'I'	     // PC is telling us stuff we don't really care about
#define SET   'T'       // as in TX from the PC => Arduino, PC is SETing our status
#define GET   'R'	     // as in TX from Arduino => PC, PC is GETing our status
#define POLL  'P'	     // PC wants to know our status
#define NOOP  0x00      // do nothing
#define STX   0x02      // start byte
#define ETX   0x03      // end byte
#define ESC   0x10      // escape byte

#define BITS_PER_BYTE 8

#include <stdio.h>
#include <stdlib.h>
#include "cmri.h"
#include "rs485bus.h"


CMRI::CMRI(int addr, RS485Bus *bus, void (*inputchange)(int, int, int), int inbytes, int outbytes) {
	numericAddr = addr;
	nodeAddr = 65 + addr;
	rs485Bus = bus;
	inputChange = inputchange;
	inBytes = inbytes;
	outBytes = outbytes;
	inBuffer =    (char *) malloc(sizeof(char) * inBytes);
	newInBuffer = (char *) malloc(sizeof(char) * inBytes);
	for (int i=0; i<inBytes; i++) {
		inBuffer[i] = 0;
		newInBuffer[i] = 0;
	}
	outBuffer =     (char *)malloc(sizeof(char) * outBytes);
	lastOutBuffer = (char *)malloc(sizeof(char) * outBytes);
	for (int i=0; i<outBytes; i++) {
		outBuffer[i] = 0;
		lastOutBuffer[i] = 0;
	}
}

void CMRI::process(void) {
	if (outputPending())
		transmit();
	poll();
}

bool CMRI::setOutputBit(int b, int v) {
	if (b <0 || b >= (outBytes*BITS_PER_BYTE)) 
		return(false);
	int byx = int(b/BITS_PER_BYTE);
	int bix = b % BITS_PER_BYTE;
	bix = BITS_PER_BYTE - 1 - bix;
	if (v != 0)
		outBuffer[byx] = outBuffer[byx] | (1 << bix) & 0xff;
	else
		outBuffer[byx] = outBuffer[byx] & ~(1 << bix) & 0xff;

	return(true);
}


bool CMRI::outputPending(void) {
	for (int i = 0; i<outBytes; i++)
		if (outBuffer[i] != lastOutBuffer[i])
			return(true);

	return(false);
}

void CMRI::transmit(void) {
	char buf[32];
	int bl = 0;
	buf[bl++] = 0xFF;
	buf[bl++] = 0xFF;
	buf[bl++] = STX;
	buf[bl++] = nodeAddr;
	buf[bl++] = SET;
	for (int i=0; i<outBytes; i++) {
		int b = outBuffer[i] % 0xFF;
		if (b == ETX) 
			buf[bl++] = ESC;
		else if (b == ESC)
			buf[bl++] = ESC;
		buf[bl++] = b;
	}	
	buf[bl++] = ETX;
	buf[bl] = '\0';
	rs485Bus -> rs485Write(buf, bl);
	rs485Bus -> rs485Flush();
	for (int i = 0; i <outBytes; i++)
		lastOutBuffer[i] = outBuffer[i];
}

void CMRI::poll(void) {
	char buf[32];
	int bl = 0;
	buf[bl++] = 0xFF;
	buf[bl++] = 0xFF;
	buf[bl++] = STX;
	buf[bl++] = nodeAddr;
	buf[bl++] = POLL;
	buf[bl++] = ETX;
	buf[bl] = '\0';
	rs485Bus -> rs485Write(buf, bl);
	rs485Bus -> rs485Flush();

	char c = 0xFF;
	while (c == (char) 0xFF) {
		int rc = rs485Bus -> rs485Read(&c, 1);
		if (rc != 0) {
			printf("Error %d from read\n", rc);
			return;
		}
	}

	if (c != STX) {
		printf("Did not get expected STX character\n");
		return;
	}

	int rc = rs485Bus -> rs485Read(&c, 1);
	if (rc != 0) {
		printf("Error %d from read\n", rc);
		return;
	}
	if (c != nodeAddr) {
		printf("Did not get expected address\n");
		return;
	}

	rc = rs485Bus -> rs485Read(&c, 1);
	if (rc != 0) {
		printf("Error %d from read\n", rc);
		return;
	}
	if (c != GET) {
		printf("Did not get expected command\n");
		return;
	}

	rc = rs485Bus -> rs485Read(&c, 1);
	if (rc != 0) {
		printf("Error %d from read\n", rc);
		return;
	}
	int bx = 0;
	while (c != ETX) {
		if (c == ESC or c == ETX)
			rs485Bus -> rs485Read(&c, 1);

		newInBuffer[bx++] = c;
		rc = rs485Bus -> rs485Read(&c, 1);
		if (rc != 0) {
			printf("Error %d from read\n", rc);
			return;
		}
	}

	printf("in buffer: ");
	for (int i=0; i<bx; i++)
		printf("%02x ", newInBuffer[i]);
	printf("\n");

	if (bx != inBytes) {
		printf("Invalid number of input bytes received - expected %d, got %d", inBytes, bx);
		return;
	}
	int offset = 0;
	for (int i = 0; i<inBytes; i++) {
		char oldb = inBuffer[i];
		char newb = newInBuffer[i];
		if (newb != oldb) {
			for (int bit=0; bit < BITS_PER_BYTE; bit++) {
				char o = oldb & (1 << BITS_PER_BYTE-1-bit);
				char n = newb & (1 << BITS_PER_BYTE-1-bit);
				if (o != n) {
					inputChange(numericAddr, bit+offset, n != 0 ? 1 : 0);
				}
			}
		}
		offset = offset + BITS_PER_BYTE;
	}

	for (int i = 0; i<inBytes; i++) {
		inBuffer[i] = newInBuffer[i];
		newInBuffer[i] = 0;
	}
}
