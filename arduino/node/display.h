#ifndef DISPLAY_H
#define DISPLAY_H


class Display {
	public:
		Display(void);
		void nodeConfig(int, int, int, int);
		void begin(void);
		bool update(void);
		void clear(void);
		void showConfig();
		void outputOn(int);
		void outputOff(int);
		void pulseOn(int, int);
		void pulseOff(int);
		void turnoutNormal(int);
		void turnoutReverse(int);
		void servoAngle(int, int);
		void message(const char *);
		void showInputChip(int, int);
		void showOutputChip(int, int);
		void showServo(int, int, int, int, int);

	private:
		char buffer[21];
		char dbuf[21];
		int addr;
		int nInputBytes;
		int nOutputBytes;
		int nServoDrivers;
		int clearTimer;
		void displayOnLine(char *, int, int);
};

#endif
