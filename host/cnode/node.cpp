#include <cstring>
#include <string>
#include <iostream>
#include <sstream>
#include <boost/log/trivial.hpp>

#include "node.h"
#include "input.h"
#include "output.h"
#include "servo.h"
#include "utils.h"

Node::Node(int a, int i, int o, int s) {
	std::stringstream n;
	n << "node" << a;
	nodeInit(n.str(), a, i, o, s);
}

Node::Node(std::string nm, int a, int i, int o, int s) {
	nodeInit(nm, a, i, o, s);
}

void Node::nodeInit(std::string nm, int a, int i, int o, int s) {
	name = nm;
	addr = a;
	ninputs = i;
	nibits = i*NIBITS;
	noutputs = o;
	nobits = o*NOBITS;
	nservos = s;
	nsbits = s*16;

	errorCount = 0;

	BOOST_LOG_TRIVIAL(info) << __func__ << ": " << "Node " << name << " at address " << addr << " created with config i:" << ninputs << "(" << nibits
					<< ")/o:" << noutputs << "(" << nobits << ")/s:" << nservos << "(" << nsbits << ")";
	for (int i=0; i<nibits; i++) {
		inputs[i] = new Input();
		inputs[i]->currentState = true;
	}
	for (int i=0; i<nobits; i++) {
		outputs[i] = new Output();
		outputs[i]->currentState = false;
	}
	for (int i=0; i<nsbits; i++) {
		servos[i] = new Servo();
	}
}

void Node::setName(std::string nm) {
	name = nm;
}

int Node::getAddr(void) {
	return addr;
}

std::string Node::GetConfig(void) {
	std::ostringstream rpt;
	rpt << "{\"name\":\"" << name << "\",\"address\":" << addr << ",\"input\":" << nibits << ",\"output\":" << nobits
		<< ",\"servo\":" << nsbits << "}";
	return rpt.str();
}

int Node::setInputStates(bool *bvals, int *idx, int n) {
	int diffs;

	diffs = 0;
	for (int i=0; i<n; i++) {
		bool bv = bvals[i];
		int ix = idx[i];

		if (ix < 0 || ix >= nibits) {
			BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "input index of " << ix << " is out of range";
			return diffs;
		}
		int ov = inputs[ix]->currentState;
		if (ov != bv) {
			diffs++;
			inputs[ix]->currentState = bv;
		}
	}
	return diffs;
}

std::string Node::InputsReport(void) {
	std::ostringstream rpt;
	rpt << "{\"inputs\":{\"address\":" << addr << ",\"count\":" << nibits << ",\"values\":[";
	for (int i = 0; i<nibits; i++) {
		if (i != 0)
			rpt << ", ";
		rpt << (inputs[i]->currentState ? "true" : "false");
	}
	rpt << "]}}";
	return rpt.str();
}

std::string Node::InputsReportDelta(int *ix, int nix) {
	std::ostringstream rpt;
	rpt << "{\"inputs\":{\"address\":" << addr << ",\"count\":" << nix << ",\"delta\":true,\"values\":[";
	for (int i = 0; i<nix; i++) {
		if (i != 0)
			rpt << ", ";
		int idx = ix[i];
		rpt << "[" << idx << ", " << (inputs[idx]->currentState ? "true" : "false") << "]";
	}
	rpt << "]}}";
	return rpt.str();
}

int Node::setOutputStates(bool *vals, int n) {
	int diffs;

	diffs = 0;
	for (int i=0; i<n; i++) {
		bool bv = vals[i];
		bool ov = outputs[i]->currentState;
		if (ov != bv) {
			diffs++;
			outputs[i]->currentState = bv;
		}
	}
	return diffs;
}

std::string Node::OutputOn(int ox) {
	std::ostringstream rpt;
	if (ox < 0 || ox >= nobits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "output index of " << ox << " is out of range";
		return "";
	}
	bool ov = outputs[ox]->currentState;
	if (ov) 
		return ""; // already on
	outputs[ox]->currentState = true;
	rpt << "{\"outputs\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"values\":[";
	rpt << "[" << ox << ", true]]}}";
	return rpt.str();
}

std::string Node::OutputOff(int ox) {
	std::ostringstream rpt;
	if (ox < 0 || ox >= nobits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "output index of " << ox << " is out of range";
		return "";
	}
	bool ov = outputs[ox]->currentState;
	if (!ov) 
		return ""; // already off
	outputs[ox]->currentState = false;
	rpt << "{\"outputs\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"values\":[";
	rpt << "[" << ox << ", false]]}}";
	return rpt.str();
}

std::string Node::OutputsReport(void) {
	std::ostringstream rpt;
	rpt << "{\"outputs\":{\"address\":" << addr << ",\"count\":" << nibits << ",\"values\":[";
	for (int i = 0; i<nobits; i++) {
		if (i != 0)
			rpt << ", ";
		rpt << (outputs[i]->currentState ? "true" : "false");
	}
	rpt << "]}}";
	return rpt.str();
}

int Node::setServoValues(short *nrm, short *rev, short *ini, short *cur, int n) {
	int diffs;

	diffs = 0;
	for (int i=0; i<n; i++) {
		if ((servos[i]->normal != nrm[i]) || (servos[i]->reverse != rev[i]) || (servos[i]->initial != ini[i]) || (servos[i]->current != cur[i]))
			diffs++;
		servos[i]->normal = nrm[i];
		servos[i]->reverse = rev[i];
		servos[i]->initial = ini[i];
		servos[i]->current = cur[i];
	}
	return diffs;
}

std::string Node::ServosReport(void) {
	std::ostringstream rpt;
	rpt << "{\"servos\":{\"address\":" << addr << ",\"count\":" << nsbits << ",\"values\":[";
	for (int i = 0; i<nsbits; i++) {
		if (i != 0)
			rpt << ", ";
		rpt << "[ " << servos[i]->normal << ", " << servos[i]->reverse << ", " << servos[i]->initial << ", " << servos[i]->current << "]";
	}
	rpt << "]}}";
	return rpt.str();
}

std::string Node::TurnoutNormal(int tx) {
	std::ostringstream rpt;
	if (tx < 0 || tx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << tx << " is out of range";
		return "";
	}
	if (servos[tx]->current == servos[tx]->normal)
		return ""; // already normal

	servos[tx]->current = servos[tx]->normal;
	rpt << "{\"servos\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"values\":[";
	rpt << "[" << tx << ", " << servos[tx]->current << "]]}}";
	return rpt.str();
}

std::string Node::TurnoutReverse(int tx) {
	std::ostringstream rpt;
	if (tx < 0 || tx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << tx << " is out of range";
		return "";
	}
	if (servos[tx]->current == servos[tx]->reverse)
		return ""; // already reverse

	servos[tx]->current = servos[tx]->reverse;
	rpt << "{\"servos\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"values\":[";
	rpt << "[" << tx << ", " << servos[tx]->current << "]]}}";
	return rpt.str();
}

bool Node::isTurnoutReversed(int tx) {
	if (tx < 0 || tx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << tx << " is out of range";
		return false;
	}
	return servos[tx]->current == servos[tx]->reverse;
}

bool Node::isTurnoutNormal(int tx) {
	if (tx < 0 || tx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << tx << " is out of range";
		return false;
	}
	return servos[tx]->current == servos[tx]->normal;
}

std::string Node::SetTurnoutLimits(int tx, int n, int r, int ini) {
	std::ostringstream rpt;
	if (tx < 0 || tx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << tx << " is out of range";
		return "";
	}
	servos[tx]->normal = n;
	servos[tx]->reverse = r;
	servos[tx]->initial = ini;
	rpt << "{\"servos\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"limits\":true,\"values\":[";
	rpt << "[" << tx << ", " << n << ", " << r << ", " << ini << "]]}}";
	return rpt.str();
}

std::string Node::ServoAngle(int sx, int ang) {
	std::ostringstream rpt;
	if (sx < 0 || sx > nsbits) {
		BOOST_LOG_TRIVIAL(error) << __func__ << ": " << "servo index of " << sx << " is out of range";
		return "";
	}
	if (servos[sx]->current == ang)
		return ""; // already at angle

	servos[sx]->current = ang;
	rpt << "{\"servos\":{\"address\":" << addr << ",\"count\":1,\"delta\":true,\"values\":[";
	rpt << "[" << sx << ", " << servos[sx]->current << "]]}}";
	return rpt.str();
}
