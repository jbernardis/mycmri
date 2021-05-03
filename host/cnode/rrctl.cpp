#include <poll.h>
#include <unistd.h>
#include <iostream>
#include <ostream>
#include <sstream>

#include <cstdlib>
#include <string>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "httpserver.h"
#include "bus.h"
#include "node.h"
#include "utils.h"
#include "config.h"


Config *cfg;
Bus *bus;

#define MAXCLIENTS 8
int clients[MAXCLIENTS];
int nClients;
struct sockaddr_in socketAddr;
int socketAddrlen;

Node * knownNodes[32];
int nNodes;

bool exitServer;


bool nodeExists(int addr) {
	for (int i=0; i<nNodes; i++)
		if (addr == knownNodes[i]->getAddr())
			return true;

	return false;
}

void delNode(int addr) {
    Node * newList[32];
    int n = 0;

    for (int i=0; i<nNodes; i++) {
        if (knownNodes[i]->getAddr() != addr) {
            newList[n++] = knownNodes[i];
		}
		else {
			Node *dn = knownNodes[i];
			delete dn;
		}
    }

    for (int i=0; i<n; i++) {
        knownNodes[i] = newList[i];
    }
    nNodes = n;
}

Node * findNode(int addr) {
	for (int i=0; i<nNodes; i++)
		if (addr == knownNodes[i]->getAddr())
			return knownNodes[i];

	return NULL;
}
	

bool sendToClient(int skt, std::string rpt) {
	short n = rpt.length();
	short nSent = send(skt, &n, sizeof(n), MSG_NOSIGNAL);
	if (nSent != sizeof(n))
		return false;
	
	nSent = send(skt, rpt.c_str(), rpt.length(), MSG_NOSIGNAL);
	if (nSent != n) 
		return false;

	return true;
}

void broadcast(std::string rpt) {
	int n;
	bool cleanup = false;
	for (int i=0; i<nClients; i++)  {
		if (!sendToClient(clients[i], rpt)) {
			std::cout << "Remote end disconnected for socket " << clients[i] << " - removing client from list" << std::endl;
			clients[i] = -1;
			cleanup = true;
		}
	}
	if (cleanup) {
		int newClients[MAXCLIENTS];
		int n = 0;
		for (int i=0; i<nClients; i++)
			if (clients[i] != -1)
				newClients[n++] = clients[i];
		for (int i=0; i<n; i++)
			clients[i] = newClients[i];
		nClients = n;
	}
}

void ProcessIdentifyResponse(int addr, int ninputs, int noutputs, int nservos) {
	if (nodeExists(addr)) {
		return;
	}

	std::string nm = cfg->GetNodeNameAtAddress(addr);
	std::cout << "retrieved node name (" << nm << ") for address " << addr << std::endl;

	Node *n = new Node(nm, addr, ninputs, noutputs, nservos);
	knownNodes[nNodes] = n;
	nNodes++;
	bus->InputCurrent(addr);
	bus->OutputCurrent(addr);
	bus->GetTurnout(addr);

	// add the node to the list of polled addresses
	bus->addNode(addr);
}

void ProcessInputResponse(int addr, bool delta, int ninput, bool* bval, int* idx) {
	Node *n = findNode(addr);
	if (n == NULL) {
		std::cerr << "input report for unknown node.  addr = " << addr << std::endl;
		return;
	}
	int diffs = n->setInputStates(bval, idx, ninput);
	if (delta) 
		broadcast(n->InputsReportDelta(idx, ninput));
	else
		broadcast(n->InputsReport());
}

void ProcessOutputResponse(int addr, int noutput, bool* val) {
	Node *n = findNode(addr);
	if (n == NULL) {
		std::cerr << "output report for unknown node.  addr = " << addr << std::endl;
		return;
	}
	int diffs = n->setOutputStates(val, noutput);
	broadcast(n->OutputsReport());
}

void ProcessTurnoutResponse(int addr, short * normal, short * reverse, short * initial, short * current, int nargs) {
	Node *n = findNode(addr); 
	if (n == NULL) {
		std::cerr << "turnout report for unknown node.  addr = " << addr << std::endl;
		return;
	}
	int diffs = n->setServoValues(normal, reverse, initial, current, nargs);
	broadcast(n->ServosReport());
}

void ProcessBusResponse(class busMessage *response) {
	int index[64];
	bool bvals[64];
	short normal[64], reverse[64], initial[64], current[64];

	int j;

	switch (response->operation) {
	case OUTPUT_CURRENT:
		if (response->nargs == 0) {
			return;
		}
		for (int i=0; i<response->nargs; i++) {
			bvals[i] = (response->args[i] != 0);
		}
		ProcessOutputResponse(response->address, response->nargs, bvals);
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

	case IDENTIFY:
		if (response->nargs != 4) {
			std::cerr << "Unexpected number of parameters in identify response" << std::endl;
			return;
		}
		ProcessIdentifyResponse((int) response->args[0], (int) response->args[1], (int) response->args[2], (int) response->args[3]);
		break;

	case GET_TURNOUT:
		j = 0;
		for (int i=0; i<response->nargs; i=i+4) {
			normal[j] = response->args[i];
			reverse[j] = response->args[i+1];
			initial[j] = response->args[i+2];
			current[j] = response->args[i+3];
			j++;
		}
		ProcessTurnoutResponse(response->address, normal, reverse, initial, current, j);
		break;

	case CONFIG:
		std::cout << "config" << std::endl;
		break;

	case ACKNOWLEDGE:
		break;

	case STORE:
		std::cout << "store" << std::endl;
		break;

	case ERRORADDRESS:
		std::cerr << "error: unexpected response from address " << response->address << ", expecting " << response->args[0] << std::endl;
		break;

	case ERRORTIMEOUT:
		std::cerr << "error: no response from address  " << response->address << std::endl;
		break;

	default:
		std::cerr << "default case in response: " << response->operation << std::endl;
	}
}

//***************************************************************************************
//
// Routines to handle bus operations initiated by HTTP requests
//
int getParameter(class httpMessage *request, std::string name) {
	for (int i = 0; i<request->nargs; i++) {
		if (name == request->names[i]) {
			return request->args[i];
		}
	}
	return -1;
}

void ProcessHttpRequest(class httpMessage *request, httpMessageBody * resp) { 
	Node *n = NULL;
	if (request->command != "/quit" && request->command != "/noderpt") {
		if (request->address < 0) {
			resp->rc = 1;
			resp->body = "node address missing";
			return;
		}
		n = findNode(request->address);
		if (n == NULL) {
			resp->rc = 1;
			resp->body = "unknown node address";
			return;
		}
	}

	if (request->command == "/outon") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		std::string r;

		r = n->OutputOn(index);
		if (r.length() != 0) {
			bus->OutputOn(request->address, index);
			broadcast(r);
		}
	}
	else if (request->command == "/outoff") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		std::string r;

		r = n->OutputOff(index);
		if (r.length() != 0) {
			bus->OutputOff(request->address, index);
			broadcast(r);
		}
	}
	else if (request->command == "/normal") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		std::string r;

		r = n->TurnoutNormal(index);
		if (r.length() != 0) {
			bus->TurnoutNormal(request->address, index);
			broadcast(r);
		}
	}
	else if (request->command == "/reverse") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		std::string r;

		r = n->TurnoutReverse(index);
		if (r.length() != 0) {
			bus->TurnoutReverse(request->address, index);
			broadcast(r);
		}
	}
	else if (request->command == "/toggle") {
		std::string r;
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		if (n->isTurnoutNormal(index)) {
			r = n->TurnoutReverse(index);
			if (r.length() != 0) {
				bus->TurnoutReverse(request->address, index);
				broadcast(r);
			}
		}
		else if (n->isTurnoutReversed(index)) {
			r = n->TurnoutNormal(index);
			if (r.length() != 0) {
				bus->TurnoutNormal(request->address, index);
				broadcast(r);
			}
		}
		resp->rc = 0;
		resp->body = "command accepted";
	}
	else if (request->command == "/angle") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}
		int angle = getParameter(request, "angle");
		if (angle < 0 || angle > 180) {
			resp->rc = 1;
			resp->body = "parameter angle missing or out of range";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		std::string r;

		r = n->ServoAngle(index, angle);
		if (r.length() != 0) {
			bus->ServoAngle(request->address, index, angle);
			broadcast(r);
		}
	}
	else if (request->command == "/getconfig") {
		resp->rc = 0;
		resp->body = n->GetConfig();
	}
	else if (request->command == "/outputs") {
		resp->rc = 0;
		resp->body = n->OutputsReport();
	}
	else if (request->command == "/inputs") {
		resp->rc = 0;
		resp->body = n->InputsReport();
	}
	else if (request->command == "/turnouts") {
		resp->rc = 0;
		resp->body = n->ServosReport();
	}
	else if (request->command == "/refresh") {
		bool inputRpt = false;
		bool outputRpt = false;
		bool turnoutRpt = false;
		if (getParameter(request, "input") != -1)
			inputRpt = true;
		if (getParameter(request, "output") != -1)
			outputRpt = true;
		if (getParameter(request, "turnout") != -1)
			turnoutRpt = true;

		if (!inputRpt && ! outputRpt && !turnoutRpt) {
			inputRpt = true;
			outputRpt = true;
			turnoutRpt = true;
		}

		if (inputRpt)
			bus->InputCurrent(request->address);

		if (outputRpt)
			bus->OutputCurrent(request->address);

		if (turnoutRpt)
			bus->GetTurnout(request->address);

		resp->rc = 0;
		resp->body = "command accepted";
	}
	else if (request->command == "/setlimits") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			return;
		}

		int normal = getParameter(request, "normal");
		if (normal < 0 || normal > 180) {
			resp->rc = 1;
			resp->body = "parameter normal missing or out of range";
			return;
		}
		int reverse = getParameter(request, "reverse");
		if (reverse < 0 || reverse > 180) {
			resp->rc = 1;
			resp->body = "parameter reverse missing or out of range";
			return;
		}
		int initial = getParameter(request, "initial");
		if (initial < 0 || initial > 180)
			initial = normal;

		std::string r;
		r = n->SetTurnoutLimits(index, normal, reverse, initial);
		if (r.length() != 0) {
			bus->SetTurnout(request->address, index, normal, reverse, initial);
			broadcast(r);
		}
		resp->rc = 0;
		resp->body = "command accepted";
	}
	else if (request->command == "/setconfig") {
		int naddr = getParameter(request, "naddr");
		if (naddr < 0) {
			resp->rc = 1;
			resp->body = "parameter naddr missing";
			return;
		}

		int inputs = getParameter(request, "inputs");
		if (inputs < 0) {
			resp->rc = 1;
			resp->body = "parameter inputs missing or out of range";
			return;
		}
		int outputs = getParameter(request, "outputs");
		if (outputs < 0) {
			resp->rc = 1;
			resp->body = "parameter outputs missing or out of range";
			return;
		}
		int servos = getParameter(request, "servos");
		if (servos < 0) {
			resp->rc = 1;
			resp->body = "parameter servos missing or out of range";
			return;
		}
		bus->Config(request->address, naddr, inputs, outputs, servos);
		resp->rc = 0;
		resp->body = "command accepted";
	}
	else if (request->command == "/noderpt") {
		resp->rc = 0;
		resp->body = "command accepted";

		std::ostringstream rpt;
		rpt << "[";
		for (int i=0; i<nNodes; i++) {
			if (i != 0)
				rpt << ", ";
			rpt << (knownNodes[i]->GetConfig());
		}
		rpt << "]";
		resp->rc = 0;
		resp->body = rpt.str();
	}
	else if (request->command == "/store") {
		resp->rc = 0;
		resp->body = "command accepted";
		bus->Store(request->address);
	}
	else if (request->command == "/init") {
		resp->rc = 0;
		resp->body = "command accepted";
		bus->delNode(request->address);
		delNode(request->address);
		bus->Identify(request->address);
	}
	else if (request->command == "/quit") {
		exitServer = true;
	}
	else {
		std::cout << "unknown http request: " << request->command << std::endl;
		resp->rc = 1;
		resp->body = "unknown command";
	}
}

int startSocketListener(const char * IPAddress, unsigned short port) {

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == 0) {
		perror("socket failed");
		exit(1);
	}

	int opt = 1;
	if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
		perror("setsocket");
		exit(1);
	}

	socketAddr.sin_family = AF_INET;
	socketAddr.sin_addr.s_addr = inet_addr(IPAddress); 
	socketAddr.sin_port = htons(port);
	if (bind(sockfd, (struct sockaddr *) &socketAddr, socketAddrlen) < 0) {
		perror("bind");
		exit(1);
	}

	if (listen(sockfd, 3) < 0) {
		perror("listen");
		exit(1);
	}
	return sockfd;
}

int main(void) {
	nClients = 0;
	socketAddrlen = sizeof(socketAddr);
	nNodes = 0;
	exitServer = false;


std::cout << "=============================================== " << sizeof(short) << std::endl;

	cfg = new Config("config.json");

	if (cfg->ConfigErrors()) {
		std::cout << "Config errors - exiting" << std::endl;
		exit(1);
	}

	const char * address = (cfg -> ipaddr).c_str();
	unsigned short httpPort = cfg -> httpport;
	unsigned short socketPort = cfg -> socketport;

	// initialize the RS485 BUS
	bus = new Bus((cfg->serialport).c_str());
	//bus->setDebug(1);
	int busRespFd = bus->getResponseFd();
	
	// initialize the HTTP server
    int pipeReq[2];
    if (pipe(pipeReq) != 0) {
        perror("HTTP request pipe");
        exit(1);
    }

    int pipeResp[2];
    if (pipe(pipeResp) != 0) {
        perror("HTTP response pipe");
        exit(1);
    }

	startHttpServer(address, httpPort, pipeReq[1], pipeResp[0]);

	int socketFd = startSocketListener(address, socketPort);

	// now sit in a loop and process events from the RS485 bus and from HTTP clients
	struct pollfd fds[3];
	fds[0].fd = busRespFd;;     // the FD on which we receive bus events
	fds[0].events = POLLIN;
    fds[1].fd = pipeReq[0];     // the FD on which we receive HTTP requests
    fds[1].events = POLLIN;
    fds[2].fd = socketFd;       // the FD from which clients subscribe for events
    fds[2].events = POLLIN;

    class httpMessage *request;
	class busMessage *response;

	// kick things off on the RS485 side by asking each node to identify itself
	for (int i=0; i<cfg->nNodes; i++) {
		std::cout << "Initializing node " << (cfg->nodeNames[i]) << " at address " << (cfg->nodeAddrs[i]) << std::endl;
		bus->Identify(cfg->nodeAddrs[i]);
	} 

	for (;;) {
		if (exitServer) {
			std::cout << "Exiting server" << std::endl;
			break;
		}
		poll(fds, 3, 250);
		if ((fds[0].revents & POLLIN)) {
			if (read(busRespFd, &response, sizeof(response)) != sizeof(response)) {
				perror("read");
			}
			else {
				ProcessBusResponse(response);
				delete response;
			}
		}
		if ((fds[1].revents & POLLIN)) {
			if (read(pipeReq[0], &request, sizeof(request)) != sizeof(request)) {
				perror("http request read");
			}
			else {
				httpMessageBody * resp = new httpMessageBody();
				ProcessHttpRequest(request, resp); 

				int rc = write(pipeResp[1], &resp, sizeof(resp));
				if (rc != sizeof(resp)) {
					perror("http response write");
					exit(1);
				}

				delete request;
			}
		}
		if ((fds[2].revents & POLLIN)) {
			int new_socket = accept(socketFd, (struct sockaddr *) & socketAddr, (socklen_t *) &socketAddrlen);
			if (new_socket < 0) {
				perror("accept");
				exit(1);
			}
			std::cout << "new socket: " << new_socket << std::endl;

			if (nClients >= MAXCLIENTS) {
				std::cerr << "Maximum clients already connected - ignoring new connection request" << std::endl;
			}
			else {
				std::string rpt;
				bool pipeError = false;
				for (int i=0; i<nNodes && !pipeError; i++) {
					Node *nd = knownNodes[i];
					if (!sendToClient(new_socket, nd->InputsReport())) {
						pipeError = true;
						break;
					}

					if (!sendToClient(new_socket, nd->OutputsReport())) {
						pipeError = true;
						break;
					}

					if (!sendToClient(new_socket, nd->ServosReport())) {
						pipeError = true;
					}
				}
				if (!pipeError) {
					clients[nClients++] = new_socket;
					std::cout << "Clients: " << nClients << std::endl;;
				}
				else {
					std::cout << "New connection ignored because of pipe error" << std::endl;
				}
			}
		}
	}
	return 0;
}




