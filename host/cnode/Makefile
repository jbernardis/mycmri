OBJECTS = rrctl.o bus.o node.o utils.o httpserver.o config.o
LIBS = -lboost_log_setup -lboost_log -lboost_thread -lpthread

rrctl: $(OBJECTS)
	g++ -static $(OBJECTS) $(LIBS) -o rrctl

all:	client rrctl

client: client.o
	g++ client.o -o client

clean:
	rm -f *.o client rrctl

backup: .backup
	tar -cvf backup/cnode.tar *.cpp *.h Makefile
	touch .backup

rrctl.o: rrctl.cpp bus.h httpserver.h node.h utils.h config.h
	g++ -c rrctl.cpp

bus.o:	bus.cpp bus.h utils.h
	g++ -c bus.cpp

node.o:	node.cpp node.h input.h output.h servo.h
	g++ -c node.cpp

httpserver.o: 	httpserver.cpp httpserver.h
	g++ -c httpserver.cpp

config.o:	config.cpp config.h
	g++ -c config.cpp

utils.o: utils.cpp
	g++ -c utils.cpp
