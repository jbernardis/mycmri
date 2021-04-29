#include "bus.h"
#include "node.h"
#include "utils.h"

Bus *bus;

Node * node[32];
int nNodes = 0;

bool nodeExists(int addr) {
	for (int i=0; i<nNodes; i++)
		if (addr == node[i]->getAddr())
			return true;

	return false;
}

Node * findNode(int addr) {
	for (int i=0; i<nNodes; i++)
		if (addr == node[i]->getAddr())
			return node[i];

	return NULL;
}
	

void ProcessIdentifyResponse(int addr, int ninputs, int noutputs, int nservos) {
	if (nodeExists(addr)) {
		return;
	}

	Node *n = new Node(addr, ninputs, noutputs, nservos);
	node[nNodes] = n;
	nNodes++;
	bus->InputCurrent(addr);
	bus->OutputCurrent(addr);

	// add the node to the list of polled addresses
	bus->addNode(addr);
}

void ProcessInputResponse(int addr, bool delta, int ninput, bool* bval, int* idx) {
	Node *n = findNode(addr);
	if (n == NULL) {
		printf("input report for unknown node.  addr = %d\n", addr);
		return;
	}
	int diffs = n->setInputStates(bval, idx, ninput);
	printf("%d changed inputs\n", diffs);
}

void ProcessOutputResponse(int addr, int noutput, int* val) {
	printf("in output callback\n");
	printf("%d data items\n", noutput);
	for (int i = 0; i<noutput; i++) {
		printf("%2d: %d\n", i, val[i]);
	}
	Node *n = findNode(addr);
	if (n == NULL) {
		printf("input report for unknown node.  addr = %d\n", addr);
		return;
	}
	int diffs = n->setOutputValues(val, noutput);
	printf("%d changed outputs\n", diffs);
}

void ProcessResponses(void) {
	int index[64];
	int vals[64];
	bool bvals[64];
	int j;
	class busMessage *response;

	for (;;) {
		response = bus->getNextResponse();
		if (response == NULL)
			break;

		switch (response->operation) {
		case OUTPUT_ON:
			printf("output on\n");
			break;

		case OUTPUT_OFF:
			printf("output off\n");
			break;

		case OUTPUT_CURRENT:
			printf("output current\n");
			printf("addr %d\n", response->address);
			printf("n: %d\n", response->nargs);
			for (int i=0; i<response->nargs; i++) {
				printf(" %2d ", response->args[i]);
			}
			printf("\n");
			if (response->nargs == 0) {
				return;
			}
			for (int i=0; i<response->nargs; i++) {
				vals[i] = response->args[i];
			}
			ProcessOutputResponse(response->address, response->nargs, vals);
			break;

		case INPUT_DELTA:
			if (response->nargs == 0) {
				return;
			}
			j = 0;
			for (int i=0; i<response->nargs; i=i+2) {
				index[j] = response->args[i];
				bvals[j] = response->args[i+1];
				j++;
			}
			ProcessInputResponse(response->address, true, j, bvals, index);
			break;

		case INPUT_CURRENT:
			for (int i=0; i<response->nargs; i++) {
				index[i] = i;
				bvals[i] = (response->args[i] != 0);
			}
			ProcessInputResponse(response->address, false, response->nargs, bvals, index);
			break;

		case TURNOUT_NORMAL:
			printf("turnout normal\n");
			break;

		case TURNOUT_REVERSE:
			printf("turnout reverse\n");
			break;

		case IDENTIFY:
			if (response->nargs != 4) {
				printf("Unexpected number of parameters in identify response\n");
				return;
			}
			ProcessIdentifyResponse((int) response->args[0], (int) response->args[1], (int) response->args[2], (int) response->args[3]);
			break;

		case SERVO_ANGLE:
			printf("servo angle\n");
			break;

		case SET_TURNOUT:
			printf("set turnout\n");
			break;

		case GET_TURNOUT:
			printf("get turnout\n");
			break;

		case CONFIG:
			printf("config\n");
			break;

		case ACKNOWLEDGE:
			printf("ack\n");
			break;

		case STORE:
			printf("store\n");
			break;

		case ERRORADDRESS:
			printf("error: unexpected response from address %d, expecting %d\n", response->address, response->args[0]);
			break;

		case ERRORTIMEOUT:
			printf("error: no response from address %d\n", response->address);
			break;

		default:
			printf("default case in response: %02x\n", response->operation);
		}

		delete response;
	}
}

int main(void) {
	bus = new Bus("/dev/ttyUSB0");
	bus->setDebug(1);
	
	bus->Identify(1);
	int cycle = 0;
	for (;;) {
		ProcessResponses();
		msleep(10);
		cycle++;
		if (cycle == 200) {
			bus->OutputOn(1, 5);
		}
		if (cycle == 500) {
			bus->OutputOn(1, 14);
		}
		if (cycle == 2000) {
			bus->OutputOff(1, 5);
		}
		if (cycle == 3000) {
			bus->TurnoutReverse(1, 0);
		}
		if (cycle == 3500) {
			bus->OutputOff(1, 14);
		}
		if (cycle == 4000) {
			bus->TurnoutNormal(1, 0);
		}
		if (cycle > 4500) break;
	}
}
