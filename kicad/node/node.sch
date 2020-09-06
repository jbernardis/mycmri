EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Interface_UART:MAX485E U2
U 1 1 5D881A60
P 5150 2850
F 0 "U2" H 4850 3300 50  0000 C CNN
F 1 "MAX485E" H 5400 2300 50  0000 C CNN
F 2 "Package_DIP:DIP-8_W7.62mm" H 5150 2150 50  0001 C CNN
F 3 "https://datasheets.maximintegrated.com/en/ds/MAX1487E-MAX491E.pdf" H 5150 2900 50  0001 C CNN
	1    5150 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5D882D31
P 6550 2850
F 0 "R1" H 6620 2896 50  0000 L CNN
F 1 "R" H 6620 2805 50  0000 L CNN
F 2 "Resistors_ThroughHole:R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical" V 6480 2850 50  0001 C CNN
F 3 "~" H 6550 2850 50  0001 C CNN
	1    6550 2850
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J6
U 1 1 5D8843CC
P 7050 2750
F 0 "J6" H 7130 2742 50  0000 L CNN
F 1 "Termination" H 7130 2651 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 7050 2750 50  0001 C CNN
F 3 "~" H 7050 2750 50  0001 C CNN
	1    7050 2750
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5D884D29
P 3400 1100
F 0 "J1" H 3480 1092 50  0000 L CNN
F 1 "Power" H 3480 1001 50  0000 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" H 3400 1100 50  0001 C CNN
F 3 "~" H 3400 1100 50  0001 C CNN
	1    3400 1100
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x05 J3
U 1 1 5D885C26
P 6300 5200
F 0 "J3" H 6380 5242 50  0000 L CNN
F 1 "Output" H 6380 5151 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Horizontal" H 6300 5200 50  0001 C CNN
F 3 "~" H 6300 5200 50  0001 C CNN
	1    6300 5200
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J2
U 1 1 5D8881D1
P 5000 5150
F 0 "J2" H 5080 5142 50  0000 L CNN
F 1 "Input" H 5080 5051 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal" H 5000 5150 50  0001 C CNN
F 3 "~" H 5000 5150 50  0001 C CNN
	1    5000 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 2850 4600 2850
Wire Wire Line
	4600 2850 4600 2900
Wire Wire Line
	4600 2950 4750 2950
Text GLabel 4250 2900 0    50   Input ~ 0
DE
Connection ~ 4600 2900
Wire Wire Line
	4600 2900 4600 2950
Text GLabel 6250 2750 0    50   Input ~ 0
B
Text GLabel 6250 2850 0    50   Input ~ 0
A
Text GLabel 5700 3050 2    50   Input ~ 0
A
Wire Wire Line
	5550 3050 5700 3050
Wire Wire Line
	5550 2750 5700 2750
Wire Wire Line
	6850 2750 6250 2750
Wire Wire Line
	6250 2850 6400 2850
Wire Wire Line
	6700 2850 6850 2850
Text GLabel 8900 5100 0    50   Input ~ 0
SCL
$Comp
L Connector_Generic:Conn_01x04 J4
U 1 1 5D88B680
P 9250 5000
F 0 "J4" H 9330 4992 50  0000 L CNN
F 1 "LCD" H 9330 4901 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal" H 9250 5000 50  0001 C CNN
F 3 "~" H 9250 5000 50  0001 C CNN
	1    9250 5000
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0103
U 1 1 5D88E749
P 4650 4850
F 0 "#PWR0103" H 4650 4700 50  0001 C CNN
F 1 "VCC" H 4667 5023 50  0000 C CNN
F 2 "" H 4650 4850 50  0001 C CNN
F 3 "" H 4650 4850 50  0001 C CNN
	1    4650 4850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5D88EBB5
P 4650 5550
F 0 "#PWR0104" H 4650 5300 50  0001 C CNN
F 1 "GND" H 4655 5377 50  0000 C CNN
F 2 "" H 4650 5550 50  0001 C CNN
F 3 "" H 4650 5550 50  0001 C CNN
	1    4650 5550
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0105
U 1 1 5D88F301
P 5950 4900
F 0 "#PWR0105" H 5950 4750 50  0001 C CNN
F 1 "VCC" H 5967 5073 50  0000 C CNN
F 2 "" H 5950 4900 50  0001 C CNN
F 3 "" H 5950 4900 50  0001 C CNN
	1    5950 4900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5D88F972
P 5950 5500
F 0 "#PWR0106" H 5950 5250 50  0001 C CNN
F 1 "GND" H 5955 5327 50  0000 C CNN
F 2 "" H 5950 5500 50  0001 C CNN
F 3 "" H 5950 5500 50  0001 C CNN
	1    5950 5500
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0107
U 1 1 5D88FED1
P 8900 4800
F 0 "#PWR0107" H 8900 4650 50  0001 C CNN
F 1 "VCC" H 8917 4973 50  0000 C CNN
F 2 "" H 8900 4800 50  0001 C CNN
F 3 "" H 8900 4800 50  0001 C CNN
	1    8900 4800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5D890832
P 8900 5300
F 0 "#PWR0108" H 8900 5050 50  0001 C CNN
F 1 "GND" H 8905 5127 50  0000 C CNN
F 2 "" H 8900 5300 50  0001 C CNN
F 3 "" H 8900 5300 50  0001 C CNN
	1    8900 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 4900 5950 5000
Wire Wire Line
	5950 5000 6100 5000
Wire Wire Line
	5950 5500 5950 5400
Wire Wire Line
	5950 5400 6100 5400
Wire Wire Line
	4650 5550 4650 5450
Wire Wire Line
	4650 5450 4800 5450
Wire Wire Line
	4650 4850 4650 4950
Wire Wire Line
	4650 4950 4800 4950
Wire Wire Line
	8900 4800 8900 4900
Wire Wire Line
	8900 4900 9050 4900
Wire Wire Line
	8900 5300 8900 5200
Wire Wire Line
	8900 5200 9050 5200
Text GLabel 8900 5000 0    50   Input ~ 0
SDA
Wire Wire Line
	8900 5000 9050 5000
Wire Wire Line
	8900 5100 9050 5100
Text GLabel 4650 5050 0    50   Input ~ 0
IDATA
Text GLabel 4650 5150 0    50   Input ~ 0
ICE
Text GLabel 4650 5250 0    50   Input ~ 0
ICLOCK
Text GLabel 4650 5350 0    50   Input ~ 0
ILATCH
Wire Wire Line
	4650 5050 4800 5050
Wire Wire Line
	4650 5150 4800 5150
Wire Wire Line
	4650 5250 4800 5250
Wire Wire Line
	4650 5350 4800 5350
Text GLabel 5950 5100 0    50   Input ~ 0
ODATA
Text GLabel 5950 5200 0    50   Input ~ 0
OCLOCK
Text GLabel 5950 5300 0    50   Input ~ 0
OLATCH
$Comp
L power:GND #PWR0113
U 1 1 5D8AB2AA
P 5150 3550
F 0 "#PWR0113" H 5150 3300 50  0001 C CNN
F 1 "GND" H 5155 3377 50  0000 C CNN
F 2 "" H 5150 3550 50  0001 C CNN
F 3 "" H 5150 3550 50  0001 C CNN
	1    5150 3550
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0114
U 1 1 5D8ABA9B
P 5150 2250
F 0 "#PWR0114" H 5150 2100 50  0001 C CNN
F 1 "VCC" H 5167 2423 50  0000 C CNN
F 2 "" H 5150 2250 50  0001 C CNN
F 3 "" H 5150 2250 50  0001 C CNN
	1    5150 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	5150 2250 5150 2350
Wire Wire Line
	5150 3450 5150 3550
Text GLabel 4250 2750 0    50   Input ~ 0
RO
Text GLabel 4250 3050 0    50   Input ~ 0
DI
$Comp
L power:GND #PWR0117
U 1 1 5D8C18F0
P 4550 1200
F 0 "#PWR0117" H 4550 950 50  0001 C CNN
F 1 "GND" H 4555 1027 50  0000 C CNN
F 2 "" H 4550 1200 50  0001 C CNN
F 3 "" H 4550 1200 50  0001 C CNN
	1    4550 1200
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0118
U 1 1 5D8C1E21
P 4400 1200
F 0 "#PWR0118" H 4400 1050 50  0001 C CNN
F 1 "VCC" H 4418 1373 50  0000 C CNN
F 2 "" H 4400 1200 50  0001 C CNN
F 3 "" H 4400 1200 50  0001 C CNN
	1    4400 1200
	-1   0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5D8C290D
P 4400 1100
F 0 "#FLG0101" H 4400 1175 50  0001 C CNN
F 1 "PWR_FLAG" H 4400 1273 50  0000 C CNN
F 2 "" H 4400 1100 50  0001 C CNN
F 3 "~" H 4400 1100 50  0001 C CNN
	1    4400 1100
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5D8C337A
P 4550 1100
F 0 "#FLG0102" H 4550 1175 50  0001 C CNN
F 1 "PWR_FLAG" H 4550 1273 50  0000 C CNN
F 2 "" H 4550 1100 50  0001 C CNN
F 3 "~" H 4550 1100 50  0001 C CNN
	1    4550 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 1100 4400 1200
Wire Wire Line
	4550 1100 4550 1200
Wire Wire Line
	5950 5100 6100 5100
Wire Wire Line
	5950 5200 6100 5200
Wire Wire Line
	5950 5300 6100 5300
$Comp
L Connector_Generic:Conn_01x02 J13
U 1 1 5D8A0704
P 4450 2400
F 0 "J13" H 4530 2392 50  0000 L CNN
F 1 "Decouple" H 4530 2301 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 4450 2400 50  0001 C CNN
F 3 "~" H 4450 2400 50  0001 C CNN
	1    4450 2400
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J14
U 1 1 5D8A0C96
P 4550 3400
F 0 "J14" H 4630 3392 50  0000 L CNN
F 1 "Decouple" H 4630 3301 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 4550 3400 50  0001 C CNN
F 3 "~" H 4550 3400 50  0001 C CNN
	1    4550 3400
	0    1    1    0   
$EndComp
Wire Wire Line
	4250 2900 4600 2900
Wire Wire Line
	4250 2750 4450 2750
Wire Wire Line
	4450 2750 4450 2600
Wire Wire Line
	4550 2600 4550 2750
Wire Wire Line
	4550 2750 4750 2750
Wire Wire Line
	4250 3050 4450 3050
Wire Wire Line
	4450 3050 4450 3200
Wire Wire Line
	4550 3200 4550 3050
Wire Wire Line
	4550 3050 4750 3050
$Comp
L power:VCC #PWR0101
U 1 1 5D8E42F8
P 3100 1000
F 0 "#PWR0101" H 3100 850 50  0001 C CNN
F 1 "VCC" H 3117 1173 50  0000 C CNN
F 2 "" H 3100 1000 50  0001 C CNN
F 3 "" H 3100 1000 50  0001 C CNN
	1    3100 1000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5D8E48CD
P 3100 1300
F 0 "#PWR0102" H 3100 1050 50  0001 C CNN
F 1 "GND" H 3105 1127 50  0000 C CNN
F 2 "" H 3100 1300 50  0001 C CNN
F 3 "" H 3100 1300 50  0001 C CNN
	1    3100 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 1200 3100 1200
Wire Wire Line
	3100 1200 3100 1300
Wire Wire Line
	3200 1100 3100 1100
Wire Wire Line
	3100 1000 3100 1100
$Comp
L MCU_Module:Arduino_Nano_v3.x A1
U 1 1 5F535CB5
P 2650 3000
F 0 "A1" H 2350 2000 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" V 2650 2950 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 2650 3000 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 2650 3000 50  0001 C CNN
	1    2650 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 2400 2050 2400
Wire Wire Line
	2150 2500 2050 2500
Wire Wire Line
	2150 2600 2050 2600
Wire Wire Line
	2150 2700 2050 2700
Wire Wire Line
	2150 2800 2050 2800
Wire Wire Line
	2150 2900 2050 2900
Wire Wire Line
	2150 3000 2050 3000
Wire Wire Line
	2150 3100 2050 3100
Wire Wire Line
	2150 3200 2050 3200
Wire Wire Line
	2150 3300 2050 3300
Wire Wire Line
	2150 3400 2050 3400
Wire Wire Line
	2150 3500 2050 3500
Wire Wire Line
	2150 3600 2050 3600
Wire Wire Line
	2150 3700 2050 3700
Wire Wire Line
	2550 2000 2550 1850
Wire Wire Line
	3150 2800 3250 2800
Wire Wire Line
	3150 3000 3250 3000
Wire Wire Line
	3150 3100 3250 3100
Wire Wire Line
	3150 3200 3250 3200
Wire Wire Line
	3150 3300 3250 3300
Wire Wire Line
	3150 3400 3250 3400
Wire Wire Line
	3150 3500 3250 3500
Wire Wire Line
	3150 3600 3250 3600
Wire Wire Line
	3150 3700 3250 3700
Wire Wire Line
	2650 4000 2650 4150
Wire Wire Line
	2650 4150 2750 4150
Wire Wire Line
	2750 4150 2750 4000
$Comp
L power:GND #PWR0111
U 1 1 5F58E393
P 2750 4150
F 0 "#PWR0111" H 2750 3900 50  0001 C CNN
F 1 "GND" H 2755 3977 50  0000 C CNN
F 2 "" H 2750 4150 50  0001 C CNN
F 3 "" H 2750 4150 50  0001 C CNN
	1    2750 4150
	1    0    0    -1  
$EndComp
Connection ~ 2750 4150
$Comp
L power:VCC #PWR0112
U 1 1 5F58E9C1
P 2550 1850
F 0 "#PWR0112" H 2550 1700 50  0001 C CNN
F 1 "VCC" H 2567 2023 50  0000 C CNN
F 2 "" H 2550 1850 50  0001 C CNN
F 3 "" H 2550 1850 50  0001 C CNN
	1    2550 1850
	1    0    0    -1  
$EndComp
NoConn ~ 2750 2000
NoConn ~ 2850 2000
NoConn ~ 3150 2400
NoConn ~ 3150 2500
Text GLabel 2050 2500 0    50   Input ~ 0
DI
Text GLabel 2050 2400 0    50   Input ~ 0
RO
Text GLabel 2050 2600 0    50   Input ~ 0
DE
Text GLabel 2050 2700 0    50   Input ~ 0
D3
Text GLabel 2050 2800 0    50   Input ~ 0
D4
Text GLabel 2050 2900 0    50   Input ~ 0
OLATCH
Text GLabel 2050 3000 0    50   Input ~ 0
OCLOCK
Text GLabel 2050 3100 0    50   Input ~ 0
ODATA
Text GLabel 2050 3200 0    50   Input ~ 0
ILATCH
Text GLabel 2050 3300 0    50   Input ~ 0
ICLOCK
Text GLabel 2050 3500 0    50   Input ~ 0
ICE
Text GLabel 2050 3600 0    50   Input ~ 0
IDATA
Text GLabel 2050 3400 0    50   Input ~ 0
D10
Text GLabel 2050 3700 0    50   Input ~ 0
D13
Text GLabel 3250 3000 2    50   Input ~ 0
A0
Text GLabel 3250 3100 2    50   Input ~ 0
A1
Text GLabel 3250 3200 2    50   Input ~ 0
A2
Text GLabel 3250 3300 2    50   Input ~ 0
A3
Text GLabel 3250 3400 2    50   Input ~ 0
SDA
Text GLabel 3250 3500 2    50   Input ~ 0
SCL
$Comp
L power:VCC #PWR0119
U 1 1 5F5A4590
P 3250 2800
F 0 "#PWR0119" H 3250 2650 50  0001 C CNN
F 1 "VCC" H 3267 2973 50  0000 C CNN
F 2 "" H 3250 2800 50  0001 C CNN
F 3 "" H 3250 2800 50  0001 C CNN
	1    3250 2800
	1    0    0    -1  
$EndComp
NoConn ~ 3250 3600
NoConn ~ 3250 3700
$Comp
L Connector:RJ45 J11
U 1 1 5F5BC7C7
P 8700 2300
F 0 "J11" H 8370 2304 50  0000 R CNN
F 1 "RJ45" H 8370 2395 50  0000 R CNN
F 2 "Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal" V 8700 2325 50  0001 C CNN
F 3 "~" V 8700 2325 50  0001 C CNN
	1    8700 2300
	-1   0    0    1   
$EndComp
$Comp
L Connector:RJ45 J12
U 1 1 5F5BECD4
P 8700 3300
F 0 "J12" H 8370 3304 50  0000 R CNN
F 1 "RJ45" H 8370 3395 50  0000 R CNN
F 2 "Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal" V 8700 3325 50  0001 C CNN
F 3 "~" V 8700 3325 50  0001 C CNN
	1    8700 3300
	-1   0    0    1   
$EndComp
Wire Wire Line
	8300 2300 8200 2300
Wire Wire Line
	8300 2400 8200 2400
Wire Wire Line
	8300 3300 8200 3300
Wire Wire Line
	8300 3400 8200 3400
Text GLabel 8200 2300 0    50   Input ~ 0
A
Text GLabel 8200 3300 0    50   Input ~ 0
A
Text GLabel 8200 2400 0    50   Input ~ 0
B
Text GLabel 8200 3400 0    50   Input ~ 0
B
Wire Wire Line
	8300 2000 7800 2000
Wire Wire Line
	7800 2000 7800 2100
Wire Wire Line
	7800 2100 8300 2100
Wire Wire Line
	8300 3000 7800 3000
Wire Wire Line
	7800 3000 7800 3100
Wire Wire Line
	7800 3100 8300 3100
$Comp
L power:GND #PWR0120
U 1 1 5F5D9A72
P 7800 3100
F 0 "#PWR0120" H 7800 2850 50  0001 C CNN
F 1 "GND" H 7805 2927 50  0000 C CNN
F 2 "" H 7800 3100 50  0001 C CNN
F 3 "" H 7800 3100 50  0001 C CNN
	1    7800 3100
	1    0    0    -1  
$EndComp
Connection ~ 7800 3100
$Comp
L power:GND #PWR0121
U 1 1 5F5DA162
P 7800 2100
F 0 "#PWR0121" H 7800 1850 50  0001 C CNN
F 1 "GND" H 7805 1927 50  0000 C CNN
F 2 "" H 7800 2100 50  0001 C CNN
F 3 "" H 7800 2100 50  0001 C CNN
	1    7800 2100
	1    0    0    -1  
$EndComp
Connection ~ 7800 2100
$Comp
L Connector_Generic:Conn_01x04 J8
U 1 1 5F5DA5DD
P 8050 5050
F 0 "J8" H 8130 5042 50  0000 L CNN
F 1 "Servo" H 8130 4951 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal" H 8050 5050 50  0001 C CNN
F 3 "~" H 8050 5050 50  0001 C CNN
	1    8050 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7850 5050 7700 5050
Wire Wire Line
	7850 5150 7700 5150
$Comp
L power:GND #PWR0122
U 1 1 5F5E8CEC
P 7150 4950
F 0 "#PWR0122" H 7150 4700 50  0001 C CNN
F 1 "GND" H 7155 4777 50  0000 C CNN
F 2 "" H 7150 4950 50  0001 C CNN
F 3 "" H 7150 4950 50  0001 C CNN
	1    7150 4950
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0123
U 1 1 5F5E959A
P 7000 5250
F 0 "#PWR0123" H 7000 5100 50  0001 C CNN
F 1 "VCC" H 7017 5423 50  0000 C CNN
F 2 "" H 7000 5250 50  0001 C CNN
F 3 "" H 7000 5250 50  0001 C CNN
	1    7000 5250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 5250 7850 5250
Wire Wire Line
	7150 4950 7850 4950
Text GLabel 7700 5050 0    50   Input ~ 0
SCL
Text GLabel 7700 5150 0    50   Input ~ 0
SDA
$Comp
L Connector_Generic:Conn_01x06 J10
U 1 1 5F5F198D
P 2200 5150
F 0 "J10" H 2280 5142 50  0000 L CNN
F 1 "Digital Pins" H 2280 5051 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 2200 5150 50  0001 C CNN
F 3 "~" H 2200 5150 50  0001 C CNN
	1    2200 5150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J9
U 1 1 5F5F2166
P 3550 5150
F 0 "J9" H 3630 5142 50  0000 L CNN
F 1 "Analog Pins" H 3630 5051 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 3550 5150 50  0001 C CNN
F 3 "~" H 3550 5150 50  0001 C CNN
	1    3550 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 4950 3200 4950
Wire Wire Line
	3200 5050 3350 5050
Wire Wire Line
	3350 5150 3200 5150
Wire Wire Line
	3350 5250 3200 5250
Wire Wire Line
	2000 4950 1850 4950
Wire Wire Line
	2000 5050 1850 5050
Wire Wire Line
	2000 5150 1850 5150
Wire Wire Line
	2000 5250 1850 5250
Text GLabel 1850 4950 0    50   Input ~ 0
D3
Text GLabel 1850 5050 0    50   Input ~ 0
D4
Text GLabel 1850 5150 0    50   Input ~ 0
D10
Text GLabel 1850 5250 0    50   Input ~ 0
D13
Text GLabel 3200 4950 0    50   Input ~ 0
A0
Text GLabel 3200 5050 0    50   Input ~ 0
A1
Text GLabel 3200 5150 0    50   Input ~ 0
A2
Text GLabel 3200 5250 0    50   Input ~ 0
A3
Wire Wire Line
	2950 5350 3350 5350
Wire Wire Line
	2950 5450 3350 5450
Wire Wire Line
	1550 5350 2000 5350
Wire Wire Line
	1550 5450 2000 5450
$Comp
L power:GND #PWR0124
U 1 1 5F63CEE0
P 1550 5450
F 0 "#PWR0124" H 1550 5200 50  0001 C CNN
F 1 "GND" H 1555 5277 50  0000 C CNN
F 2 "" H 1550 5450 50  0001 C CNN
F 3 "" H 1550 5450 50  0001 C CNN
	1    1550 5450
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0125
U 1 1 5F63D20F
P 2950 5450
F 0 "#PWR0125" H 2950 5200 50  0001 C CNN
F 1 "GND" H 2955 5277 50  0000 C CNN
F 2 "" H 2950 5450 50  0001 C CNN
F 3 "" H 2950 5450 50  0001 C CNN
	1    2950 5450
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0126
U 1 1 5F63D63E
P 1550 5350
F 0 "#PWR0126" H 1550 5200 50  0001 C CNN
F 1 "VCC" H 1567 5523 50  0000 C CNN
F 2 "" H 1550 5350 50  0001 C CNN
F 3 "" H 1550 5350 50  0001 C CNN
	1    1550 5350
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0127
U 1 1 5F63D9A5
P 2950 5350
F 0 "#PWR0127" H 2950 5200 50  0001 C CNN
F 1 "VCC" H 2967 5523 50  0000 C CNN
F 2 "" H 2950 5350 50  0001 C CNN
F 3 "" H 2950 5350 50  0001 C CNN
	1    2950 5350
	1    0    0    -1  
$EndComp
NoConn ~ 8300 2200
NoConn ~ 8300 2500
NoConn ~ 8300 2600
NoConn ~ 8300 2700
NoConn ~ 8300 3200
NoConn ~ 8300 3500
NoConn ~ 8300 3600
NoConn ~ 8300 3700
Text GLabel 5700 2750 2    50   Input ~ 0
B
Text Notes 2100 5850 2    50   ~ 0
Digital Pins
Text Notes 3450 5850 2    50   ~ 0
Analog Pins
Text Notes 4750 5850 2    50   ~ 0
Input
Text Notes 6100 5850 2    50   ~ 0
Output
Text Notes 7600 5800 2    50   ~ 0
Servo
Text Notes 8900 5750 2    50   ~ 0
LCD
$EndSCHEMATC
