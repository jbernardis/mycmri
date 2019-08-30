#ifndef INPUTBOARD_H
#define INPUTBOARD_H

#define MAX_CHIPS 8
#define BITS_PER_CHIP 8

class InputBoard {
    public:
        InputBoard(int, int, int, int, int);
        InputBoard(int, int, int, int);
        void setup(void);
        void retrieve(void);
        int getBit(int);
        int getChip(int);
        int getChipBit(int, int);

    private:
        int nChips, pLatch, pClock, pClockEnable, pData;
        int chipBits[MAX_CHIPS];
};

#endif
