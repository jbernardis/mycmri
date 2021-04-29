#ifndef NODE_H
#define NODE_H

#include "input.h"
#include "output.h"

class Node {
public:
	Node(int, int, int, int);
	int getAddr(void);
	int setInputStates(bool *, int *, int);
	int setOutputValues(int *, int);

private:
	int addr, ninputs, noutputs, nservos;
	int nibits, nobits, nsbits;

	Input *inputs[8];
	Output *outputs[8];
};

#endif
