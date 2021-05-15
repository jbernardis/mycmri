#ifndef CONFIG_H
#define CONFIG_H

class Config {
public:
	Config(std::string);
	bool ConfigErrors(void);
	std::string GetNodeNameAtAddress(int);

	std::string serialport;
	std::string ipaddr;
	short httpport;
	short socketport;
	std::string loglevel;
	std::string nodeNames[8];
	int nodeAddrs[8];
	int nNodes = 0;

private:
	bool jsonError;
};

#endif
