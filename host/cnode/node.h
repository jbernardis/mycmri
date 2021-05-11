#ifndef NODE_H
#define NODE_H

#include "input.h"
#include "output.h"
#include "servo.h"

class Node {
public:
	Node(std::string, int, int, int, int);
	Node(int, int, int, int);
	void setName(std::string);

	int getAddr(void);
	std::string GetConfig(void);

	int setInputStates(bool *, int *, int);
	std::string InputsReport(void);
	std::string InputsReportDelta(int *, int);

	int setOutputStates(bool *, int);
	std::string OutputOn(int);
	std::string OutputOff(int);
	std::string OutputsReport(void);

	int setServoValues(short *, short *, short *, short *, int);
	std::string ServosReport(void);
	std::string TurnoutReverse(int);
	std::string TurnoutNormal(int);
	std::string SetTurnoutLimits(int, int, int, int);
	bool isTurnoutNormal(int);
	bool isTurnoutReversed(int);
	std::string ServoAngle(int, int);

	int errorCount;

private:
	int addr, ninputs, noutputs, nservos;
	int nibits, nobits, nsbits;
	std::string name;
	void nodeInit(std::string, int, int, int, int);

	Input *inputs[64];
	Output *outputs[64];
	Servo *servos[64];
};

#endif
