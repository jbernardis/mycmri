#ifndef LOCOLIST_H
#define LOCOLIST_H

#define CMD_NULL   '0'
#define CMD_FOR    'f'
#define CMD_FOR128 'F'
#define CMD_REV    'r'
#define CMD_REV128 'R'
#define CMD_STOP   's'
#define CMD_ESTOP  'e'

#define MAXLOCOS 32

class LocoList{
	public:
		LocoList(void);
		bool addLoco(unsigned int, byte, byte);
		char * getLocoSpeed(int);


	private:
		int nLocos;
		int nextSlot;

		unsigned int locos[MAXLOCOS];
		byte cmds[MAXLOCOS];
		byte speeds[MAXLOCOS];
		char speedString[8];

};

#endif
