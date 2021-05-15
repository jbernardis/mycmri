#include <poll.h>
#include <unistd.h>
#include <iostream>
#include <ostream>
#include <sstream>

#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/utility/setup/console.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>

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

namespace logging = boost::log;

logging::trivial::severity_level my_log_level = logging::trivial::info;

void init_logging(std::string loglevel) {
	logging::add_console_log(std::cout, boost::log::keywords::format = "[%TimeStamp%] [%Severity%] %Message%");

	my_log_level = logging::trivial::info;
	if (loglevel == "trace")
		my_log_level = logging::trivial::trace;
	else if (loglevel == "debug")
		my_log_level = logging::trivial::debug;
	else if (loglevel == "info")
		my_log_level = logging::trivial::info;
	else if (loglevel == "warning")
		my_log_level = logging::trivial::warning;
	else if (loglevel == "error")
		my_log_level = logging::trivial::error;

    logging::core::get()->set_filter
    (
        logging::trivial::severity >= my_log_level
    );

	logging::add_common_attributes();
}

class PendingID {
public:
	int errorCount;
	int addr;
};

Config *cfg;
Bus *bus;

#define MAXCLIENTS 8
#define ERRORTHRESHOLD 10
int clients[MAXCLIENTS];
int nClients;
struct sockaddr_in socketAddr;
int socketAddrlen;

PendingID * PID[32];
int nPID;
Node * knownNodes[32];
int nNodes;

bool exitServer;

bool isConfigured(int addr) {
	for (int i=0; i<cfg->nNodes; i++) {
		if (cfg->nodeAddrs[i] == addr)
			return true;
	} 
	return false;
}

PendingID * findPID(int addr) {
	for (int i=0; i<nPID; i++)
		if (addr == PID[i]->addr)
			return PID[i];

	return NULL;
}

void delPID(int addr) {
    PendingID * newList[32];
    int n = 0;

    for (int i=0; i<nPID; i++) {
        if (PID[i]->addr != addr) {
            newList[n++] = PID[i];
		}
		else {
			PendingID *p = PID[i];
			delete p;
		}
    }

    for (int i=0; i<n; i++) {
        PID[i] = newList[i];
    }
    nPID = n;
}

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
		BOOST_LOG_TRIVIAL(info) << __func__ << ":sending to client " << i << "(socket " << clients[i] << ")";
		if (!sendToClient(clients[i], rpt)) {
			BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "Remote end disconnected for socket " << clients[i] << " - removing client from list";
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

	Node *n = new Node(nm, addr, ninputs, noutputs, nservos);
	knownNodes[nNodes] = n;
	nNodes++;

	delPID(addr);

	bus->InputCurrent(addr);
	bus->OutputCurrent(addr);
	bus->GetTurnout(addr);

	// add the node to the list of polled addresses
	bus->addNode(addr);
}

void ProcessInputResponse(int addr, bool delta, int ninput, bool* bval, int* idx) {
	Node *n = findNode(addr);
	if (n == NULL) {
		BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "input report for unknown node.  addr = " << addr;
		return;
	}
	std::string rpt;
	int diffs = n->setInputStates(bval, idx, ninput);
	if (delta) 
		rpt = n->InputsReportDelta(idx, ninput);
	else
		rpt = n->InputsReport();

	BOOST_LOG_TRIVIAL(info) << __func__ << ": Inputs Report: " << rpt;
	broadcast(rpt);
}

void ProcessOutputResponse(int addr, int noutput, bool* val) {
	Node *n = findNode(addr);
	if (n == NULL) {
		BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "output report for unknown node.  addr = " << addr;
		return;
	}
	int diffs = n->setOutputStates(val, noutput);
	std::string rpt = n->OutputsReport();
	BOOST_LOG_TRIVIAL(info) << __func__ << ": Outputs Report: " << rpt;
	broadcast(rpt);
}

void ProcessTurnoutResponse(int addr, short * normal, short * reverse, short * initial, short * current, int nargs) {
	Node *n = findNode(addr); 
	if (n == NULL) {
		BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "turnout report for unknown node.  addr = " << addr;
		return;
	}
	int diffs = n->setServoValues(normal, reverse, initial, current, nargs);
	std::string rpt = n->ServosReport();
	BOOST_LOG_TRIVIAL(info) << __func__ << ": Servos Report: " << rpt;
	broadcast(rpt);
}

void ProcessBusResponse(class busMessage *response) {
	int index[64];
	bool bvals[64];
	short normal[64], reverse[64], initial[64], current[64];

	int j;

	Node *n = findNode(response->address);

	if (response->operation == ERRORADDRESS || response->operation == ERRORTIMEOUT) {
		if (response->operation ==  ERRORADDRESS)
			BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "error: unexpected response from address " << response->address << ", expecting " << response->args[0];
		else
			BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "error: no response from address  " << response->address;

		if (n == NULL) {	
			PendingID *p = findPID(response->address);
			if (p != NULL) {
				p->errorCount++;
				if (p->errorCount > ERRORTHRESHOLD) {
					BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "too many errors from address " << response->address << ". removing from identify list.";
					delPID(response->address);
				}
				else {
					BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "Retrying identify for address " << response->address;
					bus->Identify(response->address);
				}
			}
		}
		else {
			n->errorCount++;
			if (n->errorCount > ERRORTHRESHOLD) {
				bus->delNode(response->address);
				delNode(response->address);
				BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "too many errors from address " << response->address << ". removing from poll list.";
			}
		}
		return;
	}
	else {
		if (n != NULL)
			n->errorCount = 0;
	}

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
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "Unexpected number of parameters in identify response";
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
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "Config response";
		break;

	case ACKNOWLEDGE:
		BOOST_LOG_TRIVIAL(trace) << __func__ << ": " << "ACK";
		break;

	case STORE:
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "Store response";
		break;

	default:
		BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "default case in response: " << response->operation;
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
	if (request->command != "/quit" && request->command != "/noderpt" && request->command != "/init") { 
		if (request->address < 0) {
			resp->rc = 1;
			resp->body = "node address missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "Node address missing from HTTP request";
			return;
		}
		n = findNode(request->address);
		if (n == NULL) {
			resp->rc = 1;
			resp->body = "unknown node address";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "Unknown node address in HTTP request";
			return;
		}
	}

	if (request->command == "/outon") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from outon HTTP request";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "outon HTTP request address " << request->address << " index " << index;
		std::string r;

		r = n->OutputOn(index);
		if (r.length() != 0) {
			bus->OutputOn(request->address, index);
			BOOST_LOG_TRIVIAL(info) << __func__ << ": Output On Report: " << r;
			broadcast(r);
		}
	}
	else if (request->command == "/outoff") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from outoff HTTP request";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "outoff HTTP request address " << request->address << " index " << index;
		std::string r;

		r = n->OutputOff(index);
		if (r.length() != 0) {
			bus->OutputOff(request->address, index);
			BOOST_LOG_TRIVIAL(info) << __func__ << ": Output Off Report: " << r;
			broadcast(r);
		}
	}
	else if (request->command == "/normal") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from normal HTTP request";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "normal HTTP request address " << request->address << " index " << index;
		std::string r;

		r = n->TurnoutNormal(index);
		if (r.length() != 0) {
			bus->TurnoutNormal(request->address, index);
			BOOST_LOG_TRIVIAL(info) << __func__ << ": Turnout Normal Report: " << r;
			broadcast(r);
		}
	}
	else if (request->command == "/reverse") {
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from reverse HTTP request";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "reverse HTTP request address " << request->address << " index " << index;
		std::string r;

		r = n->TurnoutReverse(index);
		if (r.length() != 0) {
			bus->TurnoutReverse(request->address, index);
			BOOST_LOG_TRIVIAL(info) << __func__ << ": Turnout Reverse Report: " << r;
			broadcast(r);
		}
	}
	else if (request->command == "/toggle") {
		std::string r;
		int index = getParameter(request, "index");
		if (index < 0) {
			resp->rc = 1;
			resp->body = "parameter index missing";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from toggle HTTP request";
			return;
		}

		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "toggle HTTP request address " << request->address << " index " << index;
		if (n->isTurnoutNormal(index)) {
			r = n->TurnoutReverse(index);
			if (r.length() != 0) {
				bus->TurnoutReverse(request->address, index);
				BOOST_LOG_TRIVIAL(info) << __func__ << ": Turnout Reverse Report: " << r;
				broadcast(r);
			}
		}
		else if (n->isTurnoutReversed(index)) {
			r = n->TurnoutNormal(index);
			if (r.length() != 0) {
				bus->TurnoutNormal(request->address, index);
				BOOST_LOG_TRIVIAL(info) << __func__ << ": Turnout Normal Report: " << r;
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
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from angle HTTP request";
			return;
		}
		int angle = getParameter(request, "angle");
		if (angle < 0 || angle > 180) {
			resp->rc = 1;
			resp->body = "parameter angle missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "angle missing from angle HTTP request";
			return;
		}

		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "angle HTTP request address " << request->address << " index " << index << " angle " << angle;
		std::string r;

		r = n->ServoAngle(index, angle);
		if (r.length() != 0) {
			bus->ServoAngle(request->address, index, angle);
			BOOST_LOG_TRIVIAL(info) << __func__ << ": Servo Angle Report: " << r;
			broadcast(r);
		}
	}
	else if (request->command == "/getconfig") {
		resp->rc = 0;
		resp->body = n->GetConfig();
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "getconfig HTTP request address " << request->address;
	}
	else if (request->command == "/outputs") {
		resp->rc = 0;
		resp->body = n->OutputsReport();
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "outputs HTTP request address " << request->address;
	}
	else if (request->command == "/inputs") {
		resp->rc = 0;
		resp->body = n->InputsReport();
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "inputs HTTP request address " << request->address;
	}
	else if (request->command == "/turnouts") {
		resp->rc = 0;
		resp->body = n->ServosReport();
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "turnouts HTTP request address " << request->address;
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

		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "refresh HTTP request address " << request->address;
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
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "index missing from setlimits HTTP request";
			return;
		}

		int normal = getParameter(request, "normal");
		if (normal < 0 || normal > 180) {
			resp->rc = 1;
			resp->body = "parameter normal missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "normal value missing from setlimits HTTP request";
			return;
		}
		int reverse = getParameter(request, "reverse");
		if (reverse < 0 || reverse > 180) {
			resp->rc = 1;
			resp->body = "parameter reverse missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "reverse value missing from setlimits HTTP request";
			return;
		}
		int initial = getParameter(request, "initial");
		if (initial < 0 || initial > 180)
			initial = normal;

		std::string r;
		r = n->SetTurnoutLimits(index, normal, reverse, initial);
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "setlimits HTTP request, address "
				<< request->address << " normal " << normal << " reverse " << reverse << " initial " << initial;
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
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "new address missing from setconfig HTTP request";
			return;
		}

		int inputs = getParameter(request, "inputs");
		if (inputs < 0) {
			resp->rc = 1;
			resp->body = "parameter inputs missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "inputs missing from setconfig HTTP request";
			return;
		}
		int outputs = getParameter(request, "outputs");
		if (outputs < 0) {
			resp->rc = 1;
			resp->body = "parameter outputs missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "outputs missing from setconfig HTTP request";
			return;
		}
		int servos = getParameter(request, "servos");
		if (servos < 0) {
			resp->rc = 1;
			resp->body = "parameter servos missing or out of range";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "servos missing from setconfig HTTP request";
			return;
		}
		bus->Config(request->address, naddr, inputs, outputs, servos);
		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "setconfig HTTP request address " << request->address << " new address " << naddr
				<< " inputs " << inputs << " outputs " << outputs << " servos " << servos;
	}
	else if (request->command == "/noderpt") {
		resp->rc = 0;
		resp->body = "command accepted";
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "noderpt HTTP request";

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
		BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "store HTTP request";
	}
	else if (request->command == "/init") {
		n = findNode(request->address);
		if (n != NULL) {
			bus->delNode(request->address);
			delNode(request->address);
		}
		if (isConfigured(request->address)) {
			bus->Identify(request->address);
			resp->rc = 0;
			resp->body = "command accepted";
			BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "init HTTP request address " << request->address;
		}
		else {
			resp->rc = 1;
			resp->body = "unknown node address";
			BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "Attempt to init non configured node address " << request->address;
		}
	}
	else if (request->command == "/quit") {
		exitServer = true;
	}
	else {
		BOOST_LOG_TRIVIAL(warning) << __func__ << ": " << "unknown http request: " << request->command;
		resp->rc = 1;
		resp->body = "unknown command";
	}
}

int startSocketListener(const char * IPAddress, unsigned short port) {

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " socket call failed";
		exit(1);
	}

	int opt = 1;
	if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " setsocket call failed";
		exit(1);
	}

	socketAddr.sin_family = AF_INET;
	socketAddr.sin_addr.s_addr = inet_addr(IPAddress); 
	socketAddr.sin_port = htons(port);
	if (bind(sockfd, (struct sockaddr *) &socketAddr, socketAddrlen) < 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " bind call failed";
		exit(1);
	}

	if (listen(sockfd, 3) < 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " listen call failed";
		exit(1);
	}
	return sockfd;
}

int main(void) {
	nClients = 0;
	socketAddrlen = sizeof(socketAddr);
	nNodes = 0;
	exitServer = false;


	cfg = new Config("config.json");

	if (cfg->ConfigErrors()) {
		std::cerr << __func__ << ": " << "Config errors - exiting" << std::endl;
		exit(1);
	}

	init_logging(cfg -> loglevel);

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
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " HTTP Request pipe creation failed";
        exit(1);
    }

    int pipeResp[2];
    if (pipe(pipeResp) != 0) {
		BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " HTTP Response pipe creation failed";
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
		BOOST_LOG_TRIVIAL(info) << __func__ << ": Initializing node " << (cfg->nodeNames[i]) << " at address " << (cfg->nodeAddrs[i]);
		PendingID *p = new PendingID();
		p->addr = cfg->nodeAddrs[i];
		p->errorCount = 0;
		PID[nPID] = p;
		nPID++;
		bus->Identify(cfg->nodeAddrs[i]);
	} 

	for (;;) {
		if (exitServer) {
			BOOST_LOG_TRIVIAL(info) << "Exiting server";
			break;
		}
		poll(fds, 3, 250);
		if ((fds[0].revents & POLLIN)) {
			if (read(busRespFd, &response, sizeof(response)) != sizeof(response)) {
				BOOST_LOG_TRIVIAL(error) << __func__ << ": error " << errno << " Bus Response pipe read failed";
			}
			else {
				ProcessBusResponse(response);
				delete response;
			}
		}
		if ((fds[1].revents & POLLIN)) {
			if (read(pipeReq[0], &request, sizeof(request)) != sizeof(request)) {
				BOOST_LOG_TRIVIAL(error) << __func__ << ": error " << errno << " HTTP Request pipe read failed";
			}
			else {
				httpMessageBody * resp = new httpMessageBody();
				ProcessHttpRequest(request, resp); 

				int rc = write(pipeResp[1], &resp, sizeof(resp));
				if (rc != sizeof(resp)) {
					BOOST_LOG_TRIVIAL(error) << __func__ << ": error " << errno << " HTTP Response pipe write failed";
					exit(1);
				}

				delete request;
			}
		}
		if ((fds[2].revents & POLLIN)) {
			int new_socket = accept(socketFd, (struct sockaddr *) & socketAddr, (socklen_t *) &socketAddrlen);
			if (new_socket < 0) {
				BOOST_LOG_TRIVIAL(fatal) << __func__ << ": error " << errno << " accept call failed";
				exit(1);
			}
			BOOST_LOG_TRIVIAL(info) << "new subscription from socket: " << new_socket;

			if (nClients >= MAXCLIENTS) {
				BOOST_LOG_TRIVIAL(warning) << "Maximum clients already connected - ignoring new connection request";
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
				}
				else {
					BOOST_LOG_TRIVIAL(error) << "New connection ignored because of pipe error";
				}
			}
		}
	}
	return 0;
}

