#ifndef RS485BUS_H
#define RS485BUS_H


class RS485Bus { 
    public: 
	    RS485Bus(char *);
		int rs485Open(void);
		int rs485Write(char *, int len=1);
		void rs485Flush(void);
		int rs485Read(char *, int len=1);
		void rs485Close(void);

	private:
		int serialPort;
		char * portName;
}; 


#endif
