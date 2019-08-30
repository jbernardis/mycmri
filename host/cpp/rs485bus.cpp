#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <linux/serial.h>

#include "rs485bus.h"

RS485Bus::RS485Bus(char * pn) {
	portName = (char *) malloc(sizeof(char *) * strlen(pn));
	strcpy(portName, pn);
}


int RS485Bus::rs485Open(void) {
	serialPort = open(portName, O_RDWR);
	if (serialPort < 0) {
		printf("Error %i from open: %s\n", errno, strerror(errno));
		return(errno);
	}

	// Configure for raw data processing
	struct termios tty;
	memset(&tty, 0, sizeof tty);
	if(tcgetattr(serialPort, &tty) != 0) {
		printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
		return(errno);
	}

	tty.c_cflag &= ~PARENB;        // Clear parity bit, disabling parity (most common)
	tty.c_cflag |= CSTOPB;         // Set stop field, two stop bit used in communication
	tty.c_cflag |= CS8;            // 8 bits per byte (most common)
	tty.c_cflag &= ~CRTSCTS;       // Disable RTS/CTS hardware flow control (most common)
	tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)

	tty.c_lflag &= ~ICANON;        // Turn off canonical processing
	tty.c_lflag &= ~ECHO;          // Disable echo
	tty.c_lflag &= ~ECHOE;         // Disable erasure
	tty.c_lflag &= ~ECHONL;        // Disable new-line echo
	tty.c_lflag &= ~ISIG;          // Disable interpretation of INTR, QUIT and SUSP
	tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
	tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes

	tty.c_oflag &= ~OPOST;         // Prevent special interpretation of output bytes (e.g. newline chars)
	tty.c_oflag &= ~ONLCR;         // Prevent conversion of newline to carriage return/line feed

	tty.c_cc[VTIME] = 50;   // tenths of a second
	tty.c_cc[VMIN] = 0;

	cfsetispeed(&tty, B19200);
	cfsetospeed(&tty, B19200);

	if (tcsetattr(serialPort, TCSANOW, &tty) != 0) {
		printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
		return(errno);
	}

	// configure for RS485 - may be unnecessary so ignore errors
	struct serial_rs485 rs485conf = {0};
	rs485conf.flags = SER_RS485_ENABLED;
	ioctl(serialPort, TIOCSRS485, &rs485conf);

	sleep(1); //required to make flush work, for some reason
	tcflush(serialPort, TCIOFLUSH);
	return(0);
}

int RS485Bus::rs485Write(char * buf, int len) {
	write(serialPort, buf, len);
	return(0);
}

void RS485Bus::rs485Flush(void) {
	tcflush(serialPort, TCOFLUSH);
}

int RS485Bus::rs485Read(char *buf, int len) {
	int num_bytes = read(serialPort, buf, len);

	if (num_bytes < 0) {
		printf("Error reading: %s", strerror(errno));
		return(errno);
	}
	return(0);
}

void RS485Bus::rs485Close(void) {
	close(serialPort);
}
