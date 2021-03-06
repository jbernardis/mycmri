#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>  
#include <poll.h>
#include <thread>
#include <iostream>
#include <sstream>
#include <mutex>
#include <boost/log/trivial.hpp>

#include "bus.h"
#include "utils.h"

std::mutex nodeList;
extern boost::log::trivial::severity_level my_log_level;

Bus::Bus(const char * portName) {
	int  baudrate = B115200;
	int status;
	struct termios ti;
	struct termios ti_prev;

	nNodes = 0;

	// Open the serial port
	busPort = open(portName, O_RDWR|O_NOCTTY);
	if (busPort < 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": " << "ERROR! Failed to open " << portName;
		exit(1);
	}

	tcgetattr(busPort, &ti_prev);    // Save the previous serial config
	tcgetattr(busPort, &ti);         // Read the previous serial config

	cfsetospeed(&ti,baudrate);  // Set the TX baud rate
	cfsetispeed(&ti,baudrate);  // Set the RX baud rate


	ti.c_cflag |= (CLOCAL | CREAD);
	ti.c_cflag &= ~PARENB;
	ti.c_cflag |= CSTOPB;
	ti.c_cflag &= ~CSIZE;
	ti.c_cflag |= CS8;
	ti.c_cflag &= ~CRTSCTS;
	ti.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
	ti.c_iflag &= ~(IXON | IXOFF | IXANY);
	ti.c_iflag |= (INPCK | ISTRIP);
	ti.c_oflag &= ~OPOST;

	ti.c_cc[VMIN] = 1;
	ti.c_cc[VTIME] = 0;

	tcsetattr(busPort, TCSANOW, &ti);  // Set the new serial config

	int pipeCmd[2];
	if (pipe(pipeCmd) != 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " during command pipe creation";
		exit(1);
	}

	int pipeResp[2];
	if (pipe(pipeResp) != 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " during response pipe creation";
		exit(1);
	}

	thrBus  = new std::thread(&Bus::busThread, this, pipeCmd[0], pipeResp[1], busPort);
	thrPoll = new std::thread(&Bus::pollThread, this, pipeCmd[1]);

	cmdQ = pipeCmd[1];
	respQ = pipeResp[0];
}

void Bus::pollThread(int fd) {
	for (int i = 0; ; i++) {
		msleep(250);
		nodeList.lock();
		for (i=0; i<nNodes; i++) {
			class busMessage *cmd = new busMessage();
			cmd->operation = POLL;
			cmd->address = nodesToPoll[i];
			cmd->nargs = 0;
			int rc = write(fd, &cmd, sizeof(cmd));

			if (rc != sizeof(cmd)) {
				BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
				exit(1);
			}

			cmd = NULL;
		}
		nodeList.unlock();
	}
}

void Bus::addNode(int addr) {
	nodeList.lock();
	nodesToPoll[nNodes] = addr;
	nNodes++;
	nodeList.unlock();
}

void Bus::delNode(int addr) {
	int newList[32];
	int n = 0;

	for (int i=0; i<nNodes; i++) {
		if (nodesToPoll[i] != addr)
			newList[n++] = nodesToPoll[i];
	}

	nodeList.lock();
	for (int i=0; i<n; i++) {
		nodesToPoll[i] = newList[i];
	}
	nNodes = n;
	nodeList.unlock();
}

void Bus::Identify(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = IDENTIFY;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::InputCurrent(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = INPUT_CURRENT;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
	}
}

void Bus::InputDelta(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = INPUT_DELTA;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::OutputCurrent(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = OUTPUT_CURRENT;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::GetTurnout(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = GET_TURNOUT;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::OutputOn(int addr, int ox) {
	class busMessage *cmd = new busMessage();
	cmd->operation = OUTPUT_ON;
	cmd->address = addr;
	cmd->nargs = 1;
	cmd->args[0] = ox;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::OutputOff(int addr, int ox) {
	class busMessage *cmd = new busMessage();
	cmd->operation = OUTPUT_OFF;
	cmd->address = addr;
	cmd->nargs = 1;
	cmd->args[0] = ox;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::TurnoutNormal(int addr, int tx) {
	class busMessage *cmd = new busMessage();
	cmd->operation = TURNOUT_NORMAL;
	cmd->address = addr;
	cmd->nargs = 1;
	cmd->args[0] = tx;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::TurnoutReverse(int addr, int tx) {
	class busMessage *cmd = new busMessage();
	cmd->operation = TURNOUT_REVERSE;
	cmd->address = addr;
	cmd->nargs = 1;
	cmd->args[0] = tx;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::ServoAngle(int addr, int sx, int ang) {
	class busMessage *cmd = new busMessage();
	cmd->operation = SERVO_ANGLE;
	cmd->address = addr;
	cmd->nargs = 2;
	cmd->args[0] = sx;
	cmd->args[1] = ang;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::SetTurnout(int addr, int tx, int norm, int rev, int initial) {
	class busMessage *cmd = new busMessage();
	cmd->operation = SET_TURNOUT;
	cmd->address = addr;
	cmd->nargs = 4;
	cmd->args[0] = tx;
	cmd->args[1] = norm;
	cmd->args[2] = rev;
	cmd->args[3] = initial;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::SetTurnout(int addr, int tx, int norm, int rev) {
	SetTurnout(addr, tx, norm, rev, norm);
}

void Bus::Config(int addr, int naddr, int inputs, int outputs, int servos) {
	class busMessage *cmd = new busMessage();
	cmd->operation = CONFIG;
	cmd->address = addr;
	cmd->nargs = 4;
	cmd->args[0] = naddr;
	cmd->args[1] = inputs;
	cmd->args[2] = outputs;
	cmd->args[3] = servos;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::Store(int addr) {
	class busMessage *cmd = new busMessage();
	cmd->operation = STORE;
	cmd->address = addr;
	cmd->nargs = 0;
	int rc = write(cmdQ, &cmd, sizeof(cmd));

	if (rc != sizeof(cmd)) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " writing to command pipe";
		exit(1);
	}
}

void Bus::busThread(int cmdQ, int respQ, int busPort) {
	struct pollfd fds[1];
	fds[0].fd = cmdQ;
	fds[0].events = POLLIN;
	class busMessage *cmd;

	char obuf[8];
	int olen;
	char ibuf[16];
	int ilen, iaddr;

	for (;;) {
		if (poll(fds, 1, -1) != 1) {
			BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " poll call failed";
			exit(1);
		}
		if (fds[0].revents != POLLIN) {
			BOOST_LOG_TRIVIAL(fatal) << __func__ << ": " << "unexpected poll revents: " << fds[0].revents;
			exit(1);
		}

		if (read(cmdQ, &cmd, sizeof(cmd)) != sizeof(cmd)) {
			BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " read from command pipe failed";
			exit(1);
		}

		obuf[0] = cmd->operation;
		for (int i = 0; i<cmd->nargs; i++)
			obuf[i+1] = cmd->args[i];
		olen = cmd->nargs+1;

		send(cmd->address, obuf, olen, ibuf, &ilen, &iaddr);
		delete cmd;

		class busMessage *resp = new busMessage();
		resp->operation = ibuf[1];
		resp->address = iaddr;
		resp->nargs = ilen - 2;
		for (int i=0; i<resp->nargs; i++) 
			resp->args[i] = ibuf[i+2];

		int rc = write(respQ, &resp, sizeof(resp));
		if (rc != sizeof(cmd)) {
			BOOST_LOG_TRIVIAL(fatal) << __func__ << ": Error " << errno << " write to response pipe failed";
			exit(1);
		}

		resp = NULL;
	}
}

int Bus::getResponseFd(void) {
	return respQ;
}

void Bus::send(char addr, const char *omsg, int n, char * ibuffer, int * ilen, int * iaddr) {
	setMode(TX);
	char obuffer[16];
	int olen = 0;

	obuffer[0] = 0xff;
	obuffer[1] = 0xff;
	obuffer[2] = STX;
	obuffer[3] = 65+addr;
	olen = 4;

	for (int i=0; i<n; i++) {
		char b = omsg[i];
		if (b == ETX || b == ESC)
			obuffer[olen++] = ESC;
		obuffer[olen++] = omsg[i];
	}
	obuffer[olen++] = ETX;

	if (my_log_level <= boost::log::trivial::trace) {
		std::stringstream lmsg;
		lmsg << "==> " << olen << " bytes:";
		for (int i=0; i<olen; i++) {
			lmsg << " " << std::hex << (obuffer[i] & 0xff);
		}
		BOOST_LOG_TRIVIAL(trace) << lmsg.str();
	}

	tcflush(busPort, TCIFLUSH);
	write(busPort, obuffer, olen);
	tcflush(busPort, TCOFLUSH);

	struct pollfd pfd;
	pfd.fd = busPort;
	pfd.events = POLLIN;

	setMode(RX);
	*ilen = -1;

	poll(&pfd, 1, 500);

	if (pfd.revents & POLLIN) {
		std::stringstream lmsg;
		if (my_log_level <= boost::log::trivial::trace) 
			lmsg << "<== ";
		
		int s, d;
		unsigned int ic;
		while((s=read(busPort, &ic, 1)) != -1) {
			if (my_log_level <= boost::log::trivial::trace) 
				lmsg << " " << std::hex << ic;

			if (ic == ESC) {
				read(busPort, &ic, 1);
				if (my_log_level <= boost::log::trivial::trace) 
					lmsg << " " << std::hex << ic;
				if (*ilen >= 0) {
					ibuffer[*ilen] = ic;
					*ilen = *ilen + 1;
				}
			}
			else if (ic == STX && *ilen == -1)
				*ilen = 0;
			else if (ic == ETX) {
				if (my_log_level <= boost::log::trivial::trace) 
					BOOST_LOG_TRIVIAL(trace) << lmsg.str();
				break;
			}
			else if (*ilen >= 0) {
				ibuffer[*ilen] = ic;
				*ilen = *ilen + 1;
			}
		}
		*iaddr = int(ibuffer[0]) - 65;
		if (addr != *iaddr) {
			BOOST_LOG_TRIVIAL(trace) << __func__ << ": " << "address mismatch - discard the message";
			*ilen = 3;
			ibuffer[1] = ERRORADDRESS;
			ibuffer[2] = addr;
		}
	}
	else {
		BOOST_LOG_TRIVIAL(trace) << __func__ << ": " << "no response";
		*ilen = 2;
		ibuffer[0] = 0;
		ibuffer[1] = ERRORTIMEOUT;
		*iaddr = addr;
	}

}

void Bus::setMode(int mode) {
	int flag = (mode == TX? 1 : 0);

	int RTS_flag;
	int DTR_flag;

	RTS_flag = TIOCM_RTS;
	DTR_flag = TIOCM_DTR;

	if (flag) {
		// TX mode
		ioctl(busPort, TIOCMBIS, RTS_flag);
		ioctl(busPort, TIOCMBIS, DTR_flag);
	}
	else {
		// RX mode
		ioctl(busPort, TIOCMBIC, RTS_flag);
		ioctl(busPort, TIOCMBIC, DTR_flag);
	}
}
