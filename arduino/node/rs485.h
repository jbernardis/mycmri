#ifndef RS485_H
#define RS485_H

#include <Arduino.h>

#define TX 'T'
#define RX 'R'

class RS485 {
	public:
		RS485(int);
		void setMode(char);
		void begin(unsigned long);
		void begin(unsigned long, uint8_t);
		void end(void);
		int available(void);
		int read(void);
		size_t write(uint8_t);
		void flush(void);

	private:
		int _dePin;
		char _mode;

};

#endif
