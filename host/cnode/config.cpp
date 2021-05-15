#include <iostream>
#include "boost/property_tree/ptree.hpp"
#include "boost/property_tree/json_parser.hpp"

#include "config.h"

Config::Config(std::string fileName) {
    using boost::property_tree::ptree;

	jsonError = false;
	bool hasSerialPort = false;
	bool hasIP = false;
	bool hasHttpPort = false;
	bool hasSocketPort = false;
	bool hasLogLevel = false;

	bool hasName;
	bool hasAddr;

    std::ifstream jsonFile(fileName);

    ptree cfg;
    read_json(jsonFile, cfg);

	for (auto & cfgparms: cfg) {
		if (cfgparms.first == "nodes") {
			for (auto & node: cfgparms.second) {
				hasName = false;
				hasAddr = false;
				for (auto & nodeparm: node.second) {
					if (nodeparm.first == "name") {
						nodeNames[nNodes] = nodeparm.second.get_value < std::string > ();
						hasName = true;
					}
					else if (nodeparm.first == "address") {
						nodeAddrs[nNodes] = nodeparm.second.get_value < short > ();
						hasAddr = true;
					}
				}
				if (hasName && hasAddr)
					nNodes++;
				else {
					std::cerr << __func__ << ": " << "JSON Config of node incomplete - need both name and address" << std::endl;
					jsonError = true;
				}
			}
		}
		else if (cfgparms.first == "serialport") {
			serialport = cfgparms.second.get_value < std::string > ();
			hasSerialPort = true;
		}
		else if (cfgparms.first == "ip") {
			ipaddr = cfgparms.second.get_value < std::string > ();
			hasIP = true;
		}
		else if (cfgparms.first == "httpport") {
			httpport = cfgparms.second.get_value < short > ();
			hasHttpPort = true;
		}
		else if (cfgparms.first == "socketport") {
			socketport = cfgparms.second.get_value < short > ();
			hasSocketPort = true;
		}
		else if (cfgparms.first == "loglevel") {
			loglevel = cfgparms.second.get_value < std::string > ();
			hasLogLevel = true;
		}
	}

	if (!hasLogLevel)
		loglevel = "info";

	if (!hasSerialPort) {
		std::cerr << __func__ << ": " << "Missing serial port name from configuration" <<std::endl;
		jsonError = true;
	}
	if (!hasIP) {
		std::cerr << __func__ << ": " << "Missing IP address from configuration" <<std::endl;
		jsonError = true;
	}
	if (!hasHttpPort) {
		std::cerr << __func__ << ": " << "Missing HTTP port number from configuration" <<std::endl;
		jsonError = true;
	}
	if (!hasSocketPort) {
		std::cerr << __func__ << ": " << "Missing Socket Listening port number from configuration" <<std::endl;
		jsonError = true;
	}
}

std::string Config::GetNodeNameAtAddress(int addr) {
	for (int i=0; i<nNodes; i++)
		if (nodeAddrs[i] == addr)
			return nodeNames[i];
	return "";
}

bool Config::ConfigErrors(void) {
	return jsonError;
}
