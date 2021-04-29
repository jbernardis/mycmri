OBJECTS = rrctl.o bus.o node.o input.o output.o utils.o
TARGET = rrctl
LIBS = -lpthread 

server: $(OBJECTS)
	g++ $(OBJECTS) $(LIBS) -o $(TARGET)

clean:
	rm -f *.o $(TARGET)

rrctl.o: rrctl.cpp bus.h
	g++ -c rrctl.cpp

bus.o:	bus.cpp bus.h utils.h
	g++ -c bus.cpp

node.o:	node.cpp node.h input.h output.h
	g++ -c node.cpp

input.o:	input.cpp input.h
	g++ -c input.cpp

output.o:	output.cpp output.h
	g++ -c output.cpp

utils.o: utils.cpp
	g++ -c utils.cpp
