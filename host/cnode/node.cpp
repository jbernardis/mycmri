#include <stdio.h>

#include "node.h"
#include "input.h"
#include "output.h"

Node::Node(int a, int i, int o, int s) {
	addr = a;
	ninputs = i;
	nibits = i*NIBITS;
	noutputs = o;
	nobits = o*NOBITS;
	nservos = s;
	nsbits = s*16;

	printf("Node at address %d created with config %d(%d)/%d(%d)/%d(%d)\n", addr, ninputs, nibits, noutputs, nobits, nservos, nsbits);
	for (int i=0; i<ninputs; i++) {
		inputs[i] = new Input();
	}
	for (int i=0; i<noutputs; i++) {
		outputs[i] = new Output();
	}
}

int Node::getAddr(void) {
	return addr;
}

int Node::setInputStates(bool *bvals, int *idx, int n) {
	int diffs;

	diffs = 0;
	for (int i=0; i<n; i++) {
		bool bv = bvals[i];
		int ix = idx[i];
		int cx = ix / NIBITS;
		int bx = ix % NIBITS;

		if (cx < 0 || cx >= ninputs) {
			printf("circuit index of %d is out of range\n", cx);
			return diffs;
		}
		int ov = inputs[cx]->getState(bx);
		if (ov != bv) {
			diffs++;
			inputs[cx]->setState(bx, bv);
		}
	}
	return diffs;
}

int Node::setOutputValues(int *vals, int n) {
	int diffs;

	diffs = 0;
	for (int i=0; i<n; i++) {
		int bv = vals[i];
		int cx = i / NOBITS;
		int bx = i % NOBITS;

		if (cx < 0 || cx >= noutputs) {
			printf("circuit index of %d is out of range\n", cx);
			return diffs;
		}
		int ov = outputs[cx]->getValue(bx);
		if (ov != bv) {
			diffs++;
			outputs[cx]->setValue(bx, bv);
		}
	}
	return diffs;
}
