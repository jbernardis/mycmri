#ifndef BUS_H
#define BUS_H

#include <thread>

#define STX  0x02
#define ETX  0x03
#define ESC  0x10

// use INPUT DELTA report for polling
#define POLL 'D'

#define OUTPUT_ON '1'
#define OUTPUT_OFF '0'
#define OUTPUT_CURRENT 'O'
#define INPUT_DELTA 'D'
#define INPUT_CURRENT 'C'
#define TURNOUT_NORMAL 'N'
#define TURNOUT_REVERSE 'R'
#define IDENTIFY 'Y'
#define SERVO_ANGLE 'A'
#define SET_TURNOUT 'T'
#define GET_TURNOUT 'G'
#define STORE 'W'
#define CONFIG 'F'

#define ACKNOWLEDGE '!'
#define ERRORTIMEOUT 't'
#define ERRORADDRESS 'a'

#define TX 1
#define RX 1

class busMessage
{
public:
	int address;
	int operation;
	char args[256];
	int nargs;
};

class Bus {
public:
	Bus(const char *);
	int getResponseFd(void);
	//void process(void);
	void join(void);
	void setDebug(int);
	void addNode(int);
	void delNode(int);
	void Identify(int);
	void InputCurrent(int);
	void InputDelta(int);
	void OutputCurrent(int);
	void GetTurnout(int);
	void OutputOn(int, int);
	void OutputOff(int, int);
	void TurnoutNormal(int, int);
	void TurnoutReverse(int, int);
	void ServoAngle(int, int, int);
	void SetTurnout(int, int, int, int, int);
	void SetTurnout(int, int, int, int);
	void Config(int, int, int, int, int);
	void Store(int);
	//class busMessage *getNextResponse(void);

private:
	void send(char, const char *, int, char *, int *, int *);
	void setMode(int);
	void pollThread(int);
	void busThread(int, int, int);

	int cmdQ, respQ;
	int busPort;
	int debug;
	std::thread *thrPoll, *thrBus;
	int nodesToPoll[32];
	int nNodes;

};

#endif
