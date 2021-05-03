#ifndef HTTP_SERVER_H
#define HTTP_SERVER_H

class httpMessage {
public:
	std::string command;
    int address;
	std::string names[16];
    int args[16];
    int nargs;
};

class httpMessageBody {
public:
	int rc;
	std::string body;
};

void startHttpServer(const char *, unsigned short, int, int);

#endif

