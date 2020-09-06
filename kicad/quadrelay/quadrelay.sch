EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "Quad Relay"
Date "2020-09-02"
Rev "1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Relay:G5LE-1 K1
U 1 1 5F46C176
P 2200 2300
F 0 "K1" V 1750 2250 50  0000 L CNN
F 1 "G5LE-1" V 2550 2150 50  0000 L CNN
F 2 "Relay_THT:Relay_SPDT_Omron-G5LE-1" H 2650 2250 50  0001 L CNN
F 3 "http://www.omron.com/ecb/products/pdf/en-g5le.pdf" H 2200 2300 50  0001 C CNN
	1    2200 2300
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J1
U 1 1 5F46E0C7
P 2250 1600
F 0 "J1" H 2330 1642 50  0000 L CNN
F 1 "Conn_01x03" H 2330 1551 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal" H 2250 1600 50  0001 C CNN
F 3 "~" H 2250 1600 50  0001 C CNN
	1    2250 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1900 2000 1750 2000
Wire Wire Line
	1900 2200 1750 2200
Wire Wire Line
	2500 2100 2600 2100
Text GLabel 1750 2000 0    50   Input ~ 0
NO1
Text GLabel 1750 2200 0    50   Input ~ 0
NC1
Text GLabel 2600 2100 2    50   Input ~ 0
W1
Text GLabel 2050 1500 0    50   Input ~ 0
NO1
Text GLabel 2050 1700 0    50   Input ~ 0
NC1
Text GLabel 2050 1600 0    50   Input ~ 0
W1
$Comp
L Relay:G5LE-1 K2
U 1 1 5F5019A3
P 3500 2300
F 0 "K2" V 3050 2250 50  0000 L CNN
F 1 "G5LE-1" V 3850 2150 50  0000 L CNN
F 2 "Relay_THT:Relay_SPDT_Omron-G5LE-1" H 3950 2250 50  0001 L CNN
F 3 "http://www.omron.com/ecb/products/pdf/en-g5le.pdf" H 3500 2300 50  0001 C CNN
	1    3500 2300
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5F5019A9
P 3550 1600
F 0 "J2" H 3630 1642 50  0000 L CNN
F 1 "Conn_01x03" H 3630 1551 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal" H 3550 1600 50  0001 C CNN
F 3 "~" H 3550 1600 50  0001 C CNN
	1    3550 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 2000 3050 2000
Wire Wire Line
	3200 2200 3050 2200
Wire Wire Line
	3800 2100 3900 2100
Text GLabel 3050 2000 0    50   Input ~ 0
NO2
Text GLabel 3050 2200 0    50   Input ~ 0
NC2
Text GLabel 3900 2100 2    50   Input ~ 0
W2
Text GLabel 3350 1500 0    50   Input ~ 0
NO2
Text GLabel 3350 1700 0    50   Input ~ 0
NC2
Text GLabel 3350 1600 0    50   Input ~ 0
W2
$Comp
L Relay:G5LE-1 K3
U 1 1 5F502F34
P 4800 2300
F 0 "K3" V 4350 2250 50  0000 L CNN
F 1 "G5LE-1" V 5150 2150 50  0000 L CNN
F 2 "Relay_THT:Relay_SPDT_Omron-G5LE-1" H 5250 2250 50  0001 L CNN
F 3 "http://www.omron.com/ecb/products/pdf/en-g5le.pdf" H 4800 2300 50  0001 C CNN
	1    4800 2300
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 5F502F3A
P 4850 1600
F 0 "J3" H 4930 1642 50  0000 L CNN
F 1 "Conn_01x03" H 4930 1551 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal" H 4850 1600 50  0001 C CNN
F 3 "~" H 4850 1600 50  0001 C CNN
	1    4850 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 2000 4350 2000
Wire Wire Line
	4500 2200 4350 2200
Wire Wire Line
	5100 2100 5200 2100
Text GLabel 4350 2000 0    50   Input ~ 0
NO3
Text GLabel 4350 2200 0    50   Input ~ 0
NC3
Text GLabel 5200 2100 2    50   Input ~ 0
W3
Text GLabel 4650 1500 0    50   Input ~ 0
NO3
Text GLabel 4650 1700 0    50   Input ~ 0
NC3
Text GLabel 4650 1600 0    50   Input ~ 0
W3
$Comp
L Relay:G5LE-1 K4
U 1 1 5F504675
P 6100 2300
F 0 "K4" V 5650 2250 50  0000 L CNN
F 1 "G5LE-1" V 6450 2150 50  0000 L CNN
F 2 "Relay_THT:Relay_SPDT_Omron-G5LE-1" H 6550 2250 50  0001 L CNN
F 3 "http://www.omron.com/ecb/products/pdf/en-g5le.pdf" H 6100 2300 50  0001 C CNN
	1    6100 2300
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J4
U 1 1 5F50467B
P 6150 1600
F 0 "J4" H 6230 1642 50  0000 L CNN
F 1 "Conn_01x03" H 6230 1551 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal" H 6150 1600 50  0001 C CNN
F 3 "~" H 6150 1600 50  0001 C CNN
	1    6150 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5800 2000 5650 2000
Wire Wire Line
	5800 2200 5650 2200
Wire Wire Line
	6400 2100 6500 2100
Text GLabel 5650 2000 0    50   Input ~ 0
NO4
Text GLabel 5650 2200 0    50   Input ~ 0
NC4
Text GLabel 6500 2100 2    50   Input ~ 0
W4
Text GLabel 5950 1500 0    50   Input ~ 0
NO4
Text GLabel 5950 1700 0    50   Input ~ 0
NC4
Text GLabel 5950 1600 0    50   Input ~ 0
W4
$Comp
L Diode:1N4148 D1
U 1 1 5F5063A9
P 2200 2900
F 0 "D1" H 2350 2850 50  0000 C CNN
F 1 "1N4148" H 2200 2750 50  0000 C CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 2200 2725 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 2200 2900 50  0001 C CNN
	1    2200 2900
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D5
U 1 1 5F50B0A7
P 1650 3100
F 0 "D5" V 1689 2982 50  0000 R CNN
F 1 "LED" V 1598 2982 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 1650 3100 50  0001 C CNN
F 3 "~" H 1650 3100 50  0001 C CNN
	1    1650 3100
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 5F50BAD4
P 1650 3500
F 0 "R1" H 1720 3546 50  0000 L CNN
F 1 "1K" H 1720 3455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical" V 1580 3500 50  0001 C CNN
F 3 "~" H 1650 3500 50  0001 C CNN
	1    1650 3500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0101
U 1 1 5F50C3DF
P 1650 2500
F 0 "#PWR0101" H 1650 2350 50  0001 C CNN
F 1 "+5V" H 1665 2673 50  0000 C CNN
F 2 "" H 1650 2500 50  0001 C CNN
F 3 "" H 1650 2500 50  0001 C CNN
	1    1650 2500
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J5
U 1 1 5F50D336
P 1250 1200
F 0 "J5" H 1330 1146 50  0000 L CNN
F 1 "Conn_01x06" H 1330 1101 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-6-5.08_1x06_P5.08mm_Horizontal" H 1250 1200 50  0001 C CNN
F 3 "~" H 1250 1200 50  0001 C CNN
	1    1250 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	1050 1200 900  1200
Wire Wire Line
	1050 1300 900  1300
Wire Wire Line
	1050 1400 900  1400
Wire Wire Line
	1050 1500 900  1500
$Comp
L power:+5V #PWR0103
U 1 1 5F50EC78
P 900 800
F 0 "#PWR0103" H 900 650 50  0001 C CNN
F 1 "+5V" H 915 973 50  0000 C CNN
F 2 "" H 900 800 50  0001 C CNN
F 3 "" H 900 800 50  0001 C CNN
	1    900  800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	1050 1100 900  1100
Wire Wire Line
	900  1100 900  1000
Connection ~ 900  1000
Wire Wire Line
	900  1000 900  800 
Text GLabel 900  1200 0    50   Input ~ 0
G1
Text GLabel 900  1300 0    50   Input ~ 0
G2
Text GLabel 900  1400 0    50   Input ~ 0
G3
Text GLabel 900  1500 0    50   Input ~ 0
G4
Wire Wire Line
	2500 2500 2600 2500
Wire Wire Line
	3800 2500 3900 2500
Wire Wire Line
	5100 2500 5200 2500
Wire Wire Line
	6400 2500 6500 2500
Text GLabel 2600 2500 2    50   Input ~ 0
G1
Text GLabel 3900 2500 2    50   Input ~ 0
G2
Text GLabel 5200 2500 2    50   Input ~ 0
G3
Text GLabel 6500 2500 2    50   Input ~ 0
G4
$Comp
L power:+5V #PWR0104
U 1 1 5F512531
P 2950 2500
F 0 "#PWR0104" H 2950 2350 50  0001 C CNN
F 1 "+5V" H 2965 2673 50  0000 C CNN
F 2 "" H 2950 2500 50  0001 C CNN
F 3 "" H 2950 2500 50  0001 C CNN
	1    2950 2500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0105
U 1 1 5F512C2D
P 4250 2500
F 0 "#PWR0105" H 4250 2350 50  0001 C CNN
F 1 "+5V" H 4265 2673 50  0000 C CNN
F 2 "" H 4250 2500 50  0001 C CNN
F 3 "" H 4250 2500 50  0001 C CNN
	1    4250 2500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0106
U 1 1 5F513191
P 5600 2500
F 0 "#PWR0106" H 5600 2350 50  0001 C CNN
F 1 "+5V" H 5615 2673 50  0000 C CNN
F 2 "" H 5600 2500 50  0001 C CNN
F 3 "" H 5600 2500 50  0001 C CNN
	1    5600 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 2500 1900 2500
Wire Wire Line
	1650 3250 1650 3350
Wire Wire Line
	1650 3650 1650 3800
Wire Wire Line
	2500 2500 2500 2900
Wire Wire Line
	2500 2900 2350 2900
Connection ~ 2500 2500
$Comp
L Diode:1N4148 D2
U 1 1 5F51C467
P 3500 2900
F 0 "D2" H 3650 2850 50  0000 C CNN
F 1 "1N4148" H 3500 2750 50  0000 C CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 3500 2725 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 3500 2900 50  0001 C CNN
	1    3500 2900
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N4148 D3
U 1 1 5F51D333
P 4800 2900
F 0 "D3" H 4950 2850 50  0000 C CNN
F 1 "1N4148" H 4800 2750 50  0000 C CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 4800 2725 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 4800 2900 50  0001 C CNN
	1    4800 2900
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N4148 D4
U 1 1 5F51DFC7
P 6100 2900
F 0 "D4" H 6250 2850 50  0000 C CNN
F 1 "1N4148" H 6100 2750 50  0000 C CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 6100 2725 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 6100 2900 50  0001 C CNN
	1    6100 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 2500 6400 2900
Wire Wire Line
	6400 2900 6250 2900
Connection ~ 6400 2500
Wire Wire Line
	5100 2500 5100 2900
Wire Wire Line
	5100 2900 4950 2900
Connection ~ 5100 2500
Wire Wire Line
	3800 2500 3800 2900
Wire Wire Line
	3800 2900 3650 2900
Connection ~ 3800 2500
$Comp
L Device:LED D6
U 1 1 5F52541C
P 2950 3150
F 0 "D6" V 2989 3032 50  0000 R CNN
F 1 "LED" V 2898 3032 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 2950 3150 50  0001 C CNN
F 3 "~" H 2950 3150 50  0001 C CNN
	1    2950 3150
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R2
U 1 1 5F525422
P 2950 3550
F 0 "R2" H 3020 3596 50  0000 L CNN
F 1 "1K" H 3020 3505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical" V 2880 3550 50  0001 C CNN
F 3 "~" H 2950 3550 50  0001 C CNN
	1    2950 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 3300 2950 3400
Wire Wire Line
	2950 3700 2950 3850
$Comp
L Device:LED D7
U 1 1 5F52725A
P 4250 3150
F 0 "D7" V 4289 3032 50  0000 R CNN
F 1 "LED" V 4198 3032 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 4250 3150 50  0001 C CNN
F 3 "~" H 4250 3150 50  0001 C CNN
	1    4250 3150
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R3
U 1 1 5F527260
P 4250 3550
F 0 "R3" H 4320 3596 50  0000 L CNN
F 1 "1K" H 4320 3505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical" V 4180 3550 50  0001 C CNN
F 3 "~" H 4250 3550 50  0001 C CNN
	1    4250 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 3300 4250 3400
Wire Wire Line
	4250 3700 4250 3850
$Comp
L Device:LED D8
U 1 1 5F529A15
P 5600 3150
F 0 "D8" V 5639 3032 50  0000 R CNN
F 1 "LED" V 5548 3032 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 5600 3150 50  0001 C CNN
F 3 "~" H 5600 3150 50  0001 C CNN
	1    5600 3150
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R4
U 1 1 5F529A1B
P 5600 3550
F 0 "R4" H 5670 3596 50  0000 L CNN
F 1 "1K" H 5670 3505 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical" V 5530 3550 50  0001 C CNN
F 3 "~" H 5600 3550 50  0001 C CNN
	1    5600 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 3300 5600 3400
Wire Wire Line
	5600 2500 5800 2500
Wire Wire Line
	4250 2500 4500 2500
Wire Wire Line
	2950 2500 3200 2500
Wire Wire Line
	1650 2900 1650 2950
Wire Wire Line
	1650 2900 2050 2900
Wire Wire Line
	1650 2500 1650 2900
Connection ~ 1650 2500
Connection ~ 1650 2900
Wire Wire Line
	2950 2500 2950 2900
Connection ~ 2950 2500
Wire Wire Line
	2950 2900 3350 2900
Connection ~ 2950 2900
Wire Wire Line
	2950 2900 2950 3000
Wire Wire Line
	4250 2900 4250 2500
Wire Wire Line
	4250 2900 4650 2900
Connection ~ 4250 2500
Wire Wire Line
	4250 3000 4250 2900
Connection ~ 4250 2900
Wire Wire Line
	5600 3000 5600 2900
Connection ~ 5600 2500
Wire Wire Line
	5600 2900 5950 2900
Connection ~ 5600 2900
Wire Wire Line
	5600 2900 5600 2500
Wire Wire Line
	1050 1000 900  1000
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5F50606F
P 900 1000
F 0 "#FLG0102" H 900 1075 50  0001 C CNN
F 1 "PWR_FLAG" V 900 1127 50  0000 L CNN
F 2 "" H 900 1000 50  0001 C CNN
F 3 "~" H 900 1000 50  0001 C CNN
	1    900  1000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5600 3700 5600 3850
Wire Wire Line
	1650 3800 2500 3800
Wire Wire Line
	2500 3800 2500 2900
Connection ~ 2500 2900
Wire Wire Line
	2950 3850 3800 3850
Wire Wire Line
	3800 3850 3800 2900
Connection ~ 3800 2900
Wire Wire Line
	4250 3850 5100 3850
Wire Wire Line
	5100 3850 5100 2900
Connection ~ 5100 2900
Wire Wire Line
	5600 3850 6400 3850
Wire Wire Line
	6400 3850 6400 2900
Connection ~ 6400 2900
$EndSCHEMATC
