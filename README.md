# mycmri
## DIY CMRI ecosystem for model railroad automation


This is very much a work in progress.  At this point, the following eagle designs are mature:



- blockocchexdelay - a single board with 6 DCC block occupancy detectors that immediately detect block entry, but do not report block exit until approximately 1 second after train actually leaves block.


All other designs are very early in their life and have not been tested/debugged:


- node - an arduino based circuit that can shift in data from many inputs, shift out data to many outputs, drive servos through a pololu maestro board, and report all of this back to a host PC (running JMRI?) via an RS485 bus.  Support for DCC Reverser and CD discharge unit is also being considered.  This circuit will also provide 5 volt power to this ecosystem.


- 2 byte input - a circuit design based on 74hc165 shift registers to pull in data from inputs such as buttons, block occupancy detectors, etc.


- 2 byte output - a circuit design based on 74hc595 shift registers to turn signals, indicators and other low current devices on or off.


- 2 byte output with darlington sink- same as above, but with a darlington array in the output stream to support other devices such as motors and relays - circuit sink.


- 2 byte output with darlington source - same as above, but with a darlington array in the output stream to support other devices such as motors and relays - circuit source.


- button debouncer - a circuit that goes between the 2 byte input and buttons to debounce those buttons.


- darlington array - a circuit that goes between a 2 byte output circuit and high current devices such as motors and relays. (an alternative to using the 2 byte output with the darlingtons incorporated)


- servo driver - an alternative to uring the expensive pololu maestro - under consideration


- others as needs/inspirations arise.

Arduino code will be provided as node functionality is implemented
