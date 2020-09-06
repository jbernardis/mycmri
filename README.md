# mycmri
## DIY CMRI ecosystem for model railroad automation


This is very much a work in progress.  At this point, the following eagle designs are mature:



- blockocchexdelay - a single board with 6 DCC block occupancy detectors that immediately detect block entry, but do not report block exit until approximately 1 second after train actually leaves block.

- 2 byte input - a circuit design based on 74hc165 shift registers to pull in data from inputs such as buttons, block occupancy detectors, etc.

- 1 byte input - a 1 shift register version of the above.

- 2 byte output with darlington open collector with a darlington array in the output stream to support other devices such as motors and relays - circuit sink.

All other designs are very early in their life and have not been tested/debugged:


- node - an arduino based circuit that can shift in data from many inputs, shift out data to many outputs, drive servos through an adafruit PWM servo driver board, and report all of this back to a host PC (running JMRI?) via an RS485 bus.    This circuit may also provide 5 volt power to this ecosystem.

- 1 byte output version of the above

- relay boards designed to work with the output boards, 2 and 4 relay variants

- others as needs/inspirations arise.  Support for DCC Reverser and CD discharge unit is also being considered.

Arduino code will be provided as node functionality is implemented

Linux-based driver code is also part of this repository and is in very early development.

Slowly moving PCB design to kicad.  Both kicad and eagle designs will be included here, at least until the first boards are fabricated and tested from the kicad designs.
