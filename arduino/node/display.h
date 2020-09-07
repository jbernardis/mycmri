#ifndef DISPLAY_H
#define DISPLAY_H


class Display {
	public:
		Display(void);
		void nodeConfig(int, int, int, int);
		void begin(void);
		void update(void);
		void clear(void);
		void showConfig();
		void outputOn(int);
		void outputOff(int);
		void turnoutNormal(int);
		void turnoutReverse(int);
		void servoAngle(int, int);
		void message(const char *);

	private:
		char buffer[21];
		int addr;
		int nInputBytes;
		int nOutputBytes;
		int nServoDrivers;
		int clearTimer;
		void displayAndTime(void);
};

#endif
