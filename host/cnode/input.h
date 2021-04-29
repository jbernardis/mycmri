#ifndef INPUT_H
#define INPUT_H

// bits/circuit
#define NIBITS 8

class Input {
public:
	Input(void);
	void setState(int, bool);
	bool getState(int);

private:
	bool currentState[NIBITS];
};

#endif
