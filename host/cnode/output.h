#ifndef OUTPUT_H
#define OUTPUT_H

// bits/circuit
#define NOBITS 8

class Output {
public:
	Output(void);
	void setValue(int, int);
	int getValue(int);

private:
	int currentValue[NOBITS];
};

#endif
