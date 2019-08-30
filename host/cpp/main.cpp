#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "rs485bus.h"
#include "cmri.h"

const char * portName = "/dev/ttyUSB0";

void inputChange(int addr, int bit, int val) {
	printf("Input has changed for %d:%d, value = %d\n", addr, bit, val);
}

int main(int argc, char **argv) {
	RS485Bus pt((char *) portName);
	int rc = pt.rs485Open();
	if (rc != 0) {
		printf("Received error code %d from RS485 open using port (%s)\n", rc, portName);
		exit(rc);
	}

	CMRI cm(0, &pt, inputChange);

	int ob = 0;
	int nb = 0;
	while (true) {
		cm.setOutputBit(ob, 0);
		cm.setOutputBit(nb, 1);

		ob = nb;
		nb = (nb +1) % 48;

		cm.process();
		usleep(250000);
	}
}
