#ifndef DISPLAY_H
#define DISPLAY_H

class Display {
	public:
		Display(int, int, int, int);
		void setup(bool state=true);
		void enable(bool);
		void clear(void);
		void showAddress();
		void showInput(int *);
		void showOutput(int *);
		void showServos(int *);

	private:
		bool enabled;
		int addr;
		int nInputBytes, nInputBits;
		int nOutputBytes, nOutputBits;
		int nServoBytes, nServoBits;
		void showData(const char *, int, int *, int);
};

#endif
