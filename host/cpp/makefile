OBJ=main.o cmri.o rs485bus.o

cmri: $(OBJ)
	g++ $(OBJ) -o cmri

.cpp.o:
	g++ -c $<

cmri.o: cmri.h rs485bus.h
main.o: rs485bus.h cmri.h
rs485bus.o: rs485bus.h

clean:
	rm *.o

backup:
	tar -cvf ../cmri.tar *.cpp *.h makefile
